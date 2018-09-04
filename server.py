import feedparser
import firebase_admin
import datetime
import time

from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import db

urls = [
    "https://www.jv.dk/rss/nyheder"
    # "https://www.tipsbladet.dk/danmark/esbjerg-fb-male/feed",
    # "https://www.jv.dk/rss/efb",
    # "https://www.bold.dk/feed/rss_by_tag/8467/",
    # "https://www.efb.dk/feed/"
]

links = []

wait_time = 60

cred = credentials.Certificate('rssnotifier-8d4ed-firebase-adminsdk-shmqn-a2d9bfc911.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://rssnotifier-8d4ed.firebaseio.com/'
})

def sendMessage(item):
    message = messaging.Message(
        token=db.reference('token').get(),
        data={
            'title': item.title,
            'link': item.link
        }
    )

    messaging.send(message)
    print ("Message sent: " + item.title)


for feed in urls:
    d = feedparser.parse(feed)
    for item in d.entries:
        links.append(item.link)

print ("Server is ready, checking for new items every " + str(wait_time) + "seconds")

time.sleep(wait_time)

while True:
    temp_items = []
    new_item = False

    for feed in urls:
        d = feedparser.parse(feed)
        for item in d.entries:
            item.feed = feed.title
            temp_items.append(item)

    for item in temp_items:
        if (links.count(item.link) == 0):
            sendMessage(item)
            new_item = True

    if (new_item):
        links = []
        for item in temp_items:
            links.append(item.link)

    time.sleep(wait_time)
