import feedparser
import firebase_admin
import datetime
import time

from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import db

urls = [
    "https://www.tipsbladet.dk/danmark/esbjerg-fb-male/feed",
    "https://www.jv.dk/rss/efb",
    "https://www.bold.dk/feed/rss_by_tag/8467/"
]

items = []

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
        items.append(item)

print ("Server is ready, checking for new items every " + str(wait_time) + "seconds")

time.sleep(wait_time)

while True:
    temp_items = []
    new_item = False

    for feed in urls:
        d = feedparser.parse(feed)
        for item in d.entries:
            temp_items.append(item)

    for item in temp_items:
        if (items.count(item) == 0):
            sendMessage(item)
            new_item = True

    if (new_item):
        items = temp_items

    time.sleep(wait_time)
