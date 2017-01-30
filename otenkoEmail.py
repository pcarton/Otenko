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

from config import serverName, username, password, woeid, fromaddr, toaddr, weatherAPI
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

#TODO change this to the http://openweathermap.org/api since yahoo is unreliable
def getHighLowWeather():
    baseurl = "api.openweathermap.org/data/2.5/weather?zip=30622,us"
    fullurl = baseurl + "&APPID=" + weatherAPI
    result, headers = urllib.request.urlretrieve(fullurl)
    print("Got Weather")
    with open(result) as weather:
        data = json.load(weather)
    forecast = data['weather']
    high = forecast['main']['temp_max']
    low = forecast['main']['temp_min']
    weather = forecast[0]['description']
    high = high*(9/5)-459.67
    low = low**(9/5)-459.67
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
    htmlWeather+=weather+"<br></p>"

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
    try:
        high,low,weather = getHighLowWeather()
    except:
        print("Could not get forcast")
        high,low,weather = "Not Available","Not Available","Not Available"
    htmlWeather, msgWeather = getWeatherMsgs(high,low,weather)
    htmlFeeds, msgFeeds = prepareEmail(masterArr)
    htmlMsg += htmlWeather+htmlFeeds+"</body></html>"
    msg += msgWeather+"\n"+msgFeeds
    sendEmail(htmlMsg, msg)
    lastrunFile = open("lastrunFile", 'wb')
    lastrun = datetime.datetime.timetuple(datetime.datetime.now())
    pickle.dump(lastrun,lastrunFile)
    lastrunFile.close()
    print("Last run at "+datetime.datetime.now().strftime("%m/%d/%Y"))

print("Starting")
run()
