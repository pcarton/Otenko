#!/usr/bin/python3.1

#TODO make config in one file
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error

import json
import smtplib
import time
import datetime
import feedparser
import pickle

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import serverName, username, password, woeid, fromaddr, toaddr, weatherAPI, zipCode, countryCode
from rssFeedClasses import rssFeed, rssItem

debug = True
verbose = True

try:
    lastrunFile = open("lastrunFile", 'rb')
    lastrun = pickle.load(lastrunFile)
    lastrunFile.close()
except:
    print("Couldn't read last run file, going with default of 3 days")
    lastrun = datetime.datetime.timetuple(datetime.datetime.now()-datetime.timedelta(3))

rssJSON = None

with open('rss-config.json', 'r+') as file:
    rssJSON = json.load(file);
file.close()

def getHighLowWeather():
    baseurl = "http://api.openweathermap.org/data/2.5/forecast/daily?zip="+zipCode+","+countryCode+"&cnt=1"
    fullurl = baseurl + "&APPID=" + weatherAPI
    result = urllib.request.Request(fullurl)
    resultJSON = urllib.request.urlopen(fullurl).read().decode('ascii','ignore')
    data = json.loads(resultJSON)
    print("Got Weather")
    #print(data)
    high = data['list'][0]['temp']['max']
    low = data['list'][0]['temp']['min']
    weather = data['list'][0]['weather'][0]['description'].title()
    high = high * (9/5) - 459.67
    high = '{:.0f}'.format(high)
    low = low * (9/5) - 459.67
    low = '{:.0f}'.format(low)
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
    global debug, verbose
    articleDate = None
    try:
        articleDate = item.published_parsed
    except AttributeError as e:
        try:
            articleDate = item.updated_parsed
        except AttributeError as e:
            print("No published or updated date")
    try:
        if not articleDate is None and articleDate>=lastrun:
            title = item.title.encode('ascii',"ignore")
            link = item.link.encode('ascii',"ignore")
            if verbose or debug:
                print("New Article")
                print(title)
                print(link)
            return title, link
        elif verbose or debug:
            print("Not adding this item as it was published befor lastrun")
            print(item.title.encode('ascii',"ignore"))
            print(item.link.encode('ascii',"ignore"))
            print(articleDate)
            return None,None
        else:
            return None, None
    except TypeError as e:
        print("TypeError on comparing dates")
        print(e)

def parseFeed(feedURL, feedName, feedNumToRead):
    feed = feedparser.parse(feedURL)
    feedObj = rssFeed(feedName,None)
    for item in feed["items"]:
        try:
            title, link = parseFeedItem(item)
            if not title == None and not link == None:
                feedObj.appendToFeed(title,link)
        except AttributeError as e:
            print('Exception on item in feed: '+ feedName)
            print(e)
            break
        if not (len(feedObj.getItems()) < feedNumToRead or feedNumToRead == -1):
            break

    print("Parsed "+feedName)
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
    if(not debug):
        sendEmail(htmlMsg, msg)
        lastrunFile = open("lastrunFile", 'wb')
        now =  datetime.datetime.utcnow()
        lastrun = now.utctimetuple()
        pickle.dump(lastrun,lastrunFile)
        lastrunFile.close()
        print("Last run at "+now.strftime("%m/%d/%Y %H:%M:%S UTC"))

print("Starting")
run()
