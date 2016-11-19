# Otenko
A collection of personal assistant type scripts and automations

## Email Notifications
These are emails of news, weather, and other web content that are sent daily. Most are gathered from RSS feeds.
To use this module, you need to edit two files, 'rss-config-EXAMPLE.json' and 'config.py.txt' in the following ways:
###Edit the code blocks in the .json file 
Include the name, url, and number of items from each feed to get each time its run
Those blocks look like this:
~~~
{
      "name": "",
      "url":"",
      "numMostRecent":-1
    },
~~~
The comma at the end is not nessesary on the last block.
Rename the file to 'rss-config.json' when you are done

###Edit the config.py.txt 
Include the ip of your mail server (gmail works) and your username, password for that server.
The woeid is your location id as used for Yahoo api lookups.
Also add the address you are sending from and the address you want the mail delivered to
Finally, rename the file to 'config.py'
