class rssFeed(object):
    def __init__(self,name,itemsArr):
        self.name = name
        if(not itemsArr == None):
            self.itemsArr = itemsArr
        else:
            self.itemsArr = []

    def getName(self):
        return self.name

    def getItems(self):
        return self.itemsArr

    def appendToFeed(self,title,link):
        item = rssItem(title,link)
        self.itemsArr.append(item)

class rssItem(object):
    def __init__(self,title,link):
        self.title = title
        self.link = link

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link
