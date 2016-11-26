#!/usr/bin/python3.1
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error

import json
import smtplib
import time
import datetime
import feedparser
import pickle

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import serverName, username, password, woeid, fromaddr, toaddr
from rssFeedClasses import rssFeed, rssItem

lastrunFile = open("lastrunFile", 'rb')
try:
    lastrun = pickle.load(lastrunFile)
except EOFError:
    print("Couldn't read last run file, going with default of 1 day")
    lastrun = datetime.datetime.timetuple(datetime.datetime.now()-datetime.timedelta(1))
lastrunFile.close()

rssJSON = None

with open('rss-config.json', 'r+') as file:
    rssJSON = json.load(file);
file.close()

def getHighLowWeather():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\""+woeid+"\")"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result, headers = urllib.request.urlretrieve(yql_url)
    print("Got Weather")
    with open(result) as weather:
        data = json.load(weather)
    forecast = data['query']['results']['channel']['item']['forecast'][0]
    high = forecast['high']
    low = forecast['low']
    weather = forecast['text']
    return (high,low,weather)

def getWeatherMsgs(high,low,weather):
    htmlWeather = ""
    msgWeather =""

    msgWeather+="Weather \n \t High is:"+high
    msgWeather+="\n \t Low is:"+low
    msgWeather+="\n \t Conditions are:"+weather

    htmlWeather+="<h2>Weather</h2>"
    htmlWeather+="<p>High is: "+ high+"<br>"
    htmlWeather+="Low is: "+ low+"<br>"
    htmlWeather+="Conditions are: "+ weather+"<br></p>"

    return htmlWeather, msgWeather

def parseFeedItem(item):
    global lastrun
    articleDate = item.published_parsed
    if articleDate>lastrun:
        title = item.title.encode('ascii',"ignore")
        link = item.link.encode('ascii',"ignore")
        return title, link
    else:
        return None,None

def parseFeed(feedURL, feedName, feedNumToRead):
    feed = feedparser.parse(feedURL)
    print("Parsed "+feedName)
    feedObj = rssFeed(feedName,None)
    for item in feed["items"]:
        try:
            title, link = parseFeedItem(item)
            if not title == None and not link == None:
                feedObj.appendToFeed(title,link)
        except AttributeError:
            break
        if (not feedNumToRead==-1) and len(feedObj.getItems())>feedNumToRead:
            break
    return feedObj

def prepareEmail(masterArr):
    htmlMsg = ""
    msg = ""
    for feed in masterArr:
        name = feed.getName()
        msg+=name+"\n"
        if len(feed.getItems())>0:
            htmlMsg+="<h2>"+name+"</h2>"
            htmlMsg+="<ul style=\"list-style-type:square\">"
            for item in feed.getItems():
                title = item.getTitle().decode('UTF-8')
                link = item.getLink().decode('UTF-8')
                msg+="\t"+ title +"\n"
                msg+="\t"+ link +"\n"
                htmlMsg+="<li><a href=\""+link+"\">"+title+"</a></li><br>"
                msg+="\n"
                htmlMsg+="</ul>"
    return htmlMsg, msg

def sendEmail(htmlMsg, msg):
    mime = MIMEMultipart('alternative')
    mime['Subject'] = str(datetime.date.today())
    mime['From'] = "OtenkoBot"
    mime['To'] = toaddr

    part1 = MIMEText(msg,'plain')
    part2 = MIMEText(htmlMsg, 'html')

    mime.attach(part1)
    mime.attach(part2)

    server = smtplib.SMTP(serverName)
    server.starttls()
    server.login(username, password)

    header = 'Subject: %s\n\n' % datetime.date.today()

    server.sendmail(fromaddr,toaddr,mime.as_string())
    server.quit()

def run():
    global lastrun, lastrunFile
    masterArr = []
    htmlMsg = "<html><head></head><body>"
    msg = ""
    for feed in rssJSON["feeds"]:
        tempObj = parseFeed(feed["url"], feed["name"], feed["numMostRecent"])
        masterArr.append(tempObj)
    high,low,weather = getHighLowWeather()
    htmlWeather, msgWeather = getWeatherMsgs(high,low,weather)
    htmlFeeds, msgFeeds = prepareEmail(masterArr)
    htmlMsg += htmlWeather+htmlFeeds+"</body></html>"
    msg += msgWeather+"\n"+msgFeeds
    sendEmail(htmlMsg, msg)
    lastrunFile = open("lastrunFile", 'wb')
    lastrun = datetime.date.today()
    pickle.dump(lastrun,lastrunFile)
    lastrunFile.close()
    print("Last run at "+datetime.datetime.now().strftime("%m/%d/%Y"))

print("Starting")
run()
