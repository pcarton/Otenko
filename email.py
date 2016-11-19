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

lastrunFile = open("lastrunFile", 'r+')
lastrun = pickle.load(lastrunFile)

rssJSON = None

with open('rss-config.json', 'r') as file:
    rssJSON = json.load(file);
file.close()

def getHighLowWeather():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"Bogart,GA\")"
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

def parseFeedItem(item):
    if articleDate>lastrun:
        title = item.title.encode('ascii',"ignore")
        link = item.link.encode('ascii',"ignore")
    return(title, link)

def parseFeed(feedURL, feedName, feedNumToRead):
    feed = feedparser.parse(feedURL)
    print("Parsed "+feedName)
    feedArr = []
    for item in feed["items"]:
        try:
            title, link = parseFeedItem(item)
            feed.append(title,link)
        except AttributeError:
            break
        if(feedNumToRead!=-1 && len(feedArr)>feedNumToRead)
            break
    return (feedArr)

def prepareEmail(arr):
    #TODO implement, use markup.py

def sendEmail():
    #TODO implement

def run():
    global lastrun
    masterArr = []
    for feed in rssJSON["feeds"]:
        tempArr = parseFeed(feed["url"], feed["name"], feed["numMostRecent"])
        masterArr.append(tempArr)
    prepareEmail(masterArr)
    sendEmail()
    lastrun = datetime.datetime.timetuple(datetime.datetime.now())
    pickle.dump(lastrun,lastrunFile)
    print("Last run at "+lastrun.strftime('%m/%d/%Y'))

print("Starting")
run()

lastrunFile.close()
