import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import pyrebase

cred = credentials.Certificate('./serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://t-space-1616840866880-default-rtdb.firebaseio.com/'
})

config = {
    "apiKey": "AIzaSyBytnj22REer1KkXEh7hE3n-UEaWbd4Cko",
    "authDomain": "t-space-1616840866880.firebaseapp.com",
    "databaseURL": "https://t-space-1616840866880-default-rtdb.firebaseio.com",
    "projectId": "t-space-1616840866880",
    "storageBucket": "t-space-1616840866880.appspot.com",
    "messagingSenderId": "480566478333",
    "appId": "1:480566478333:web:2483f90f24c24f274f8594",
    "measurementId": "G-1SDZS9ETT0",
    "serviceAccount": "./serviceAccount.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

uref = db.reference("/Users/")
aref = db.reference("/Admins/")
tref = db.reference("/Therapists/")

pendingusref = db.reference("/Pending-Users/")
pendingtref = db.reference("/Pending-Therapists/")

sref = db.reference("/Stories/")
slpref = db.reference("/Stories-LP/")
sarchiveref = db.reference("/Stories-Archive/")
cref = db.reference("/Comments/")
commentarchiveref = db.reference("/Comments-Archive/")

tmref = db.reference("/Unconfirmed-Meetings/")
mref = db.reference("/Meetings/")
pmref = db.reference("/Past-Meetings/")

utref = db.reference("/User->Therapist/")

nref = db.reference("/Notifications/")
utransref = db.reference("/Unconfirmed-Transactions/")
transref = db.reference("/Transactions/")

storageRef = firebase.storage()
bucket = storage.bucket("t-space-1616840866880.appspot.com")
pyre_db = firebase.database()

refer = {
    'user':uref,
    'therapist':tref,
    'admin':aref
}