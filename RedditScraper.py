import requests
from bs4 import BeautifulSoup
from enum import Enum
import random

def GetParsedPage(url, parser = "lxml"):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = headers)
    return BeautifulSoup(page.content, parser)

class RedditFilterType(Enum):
    Hot = 0
    New = 1
    TopHour = 2
    TopDay = 3
    TopWeek = 4
    TopMonth = 5
    TopYear = 6
    TopAllTime = 7
    Rising = 8

def GetRedditPosts(subreddit = "popular", numberOfResults = 10, filterType = RedditFilterType.Hot): #Returns list of URLs for top _numberOfResults_ posts on _subreddit_ filtered by _filterType_
    filterStrings = ["/hot.xml?limit=","/new.xml?limit=","/top.xml?t=hour&limit=","/top.xml?t=day&limit=","/top.xml?t=week&limit=","/top.xml?t=month&limit=","/top.xml?t=year&limit=","/top.xml?t=all&limit=","/rising.xml?limit="]
    resultList = []

    if(numberOfResults > 100):
        numberOfResults = 100

    soup = GetParsedPage("https://www.reddit.com/r/" + subreddit + filterStrings[filterType.value] + str(numberOfResults), "xml")
    rawResultList = soup.find_all(name="entry")
    for rawResult in rawResultList:
        resultList.append(BeautifulSoup(rawResult.find_all(name="content")[0].contents[0], "lxml").find_all("a")[-1].get("href"))
    
    return resultList

def GetRedditPostData(postURL): #Takes a URL for a certain reddit post and returns a tuple containing the title and the body(text only if applicaple) of the post. Format: (title, body)
    soup = GetParsedPage(postURL)

    postTitle = soup.find_all("shreddit-post")[0].find_all("h1")[0].text.strip()
    rawPostBody = soup.find_all("shreddit-post")[0].find_all("p")
    postBody = ""

    for i in range(1, len(rawPostBody)):
        postBody += rawPostBody[i].text.strip() + "\n"
    
    return (postTitle, postBody.strip())

def SaveRedditPostDataToFile(postText, filename = "Reddit Post #", directoryPath = ""):
    if(filename == "Reddit Post #"):
        filename += str(random.randrange(1000))
    
    if(filename[len(filename) - 4:] != ".txt"):
        filename += ".txt"
    
    if(directoryPath != "" and directoryPath[-1] != "\\"):
        directoryPath += "\\"
    file = open(directoryPath + filename, "w")
    file.write(postText[0] + "\n" + postText[1])
    file.close()

