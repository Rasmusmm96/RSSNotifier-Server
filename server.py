import firebase_admin

from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import db

cred = credentials.Certificate('rssnotifier-8d4ed-firebase-adminsdk-shmqn-a2d9bfc911.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://rssnotifier-8d4ed.firebaseio.com/'
})

token = db.reference('token').get()

message = messaging.Message(
    token=token,
    android=messaging.AndroidConfig(
        notification=messaging.AndroidNotification(
            title='News',
            body='Test'
        ),
    )
)

# Send a message to the device corresponding to the provided
# registration token.
response = messaging.send(message)
# Response is a message ID string.
print('Successfully sent message:', response)
