from flask import session, render_template, request, redirect
from functools import wraps
from firebaseref.firebasereference import sref, sarchiveref, pendingusref, mref, pmref, nref
import random
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                return render_template('index.html',redirected='True',showmodal='#signinmodal')
        except Exception as e:
            print(str(e))
            return render_template('index.html',redirected='True',showmodal='#signinmodal')
    return wrap

def generate_id(initial):
    return initial+datetime.now(IST).strftime('%Y%m%d%H%M%S')

def is_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if session['user_type']== 'user':
                return f(*args, **kwargs)
            else:
                return render_template('index.html',msg='You are not authorized to access the page.')
        except Exception as e:
            return render_template('index.html',msg='You are not authorized to access the page.')
    return wrap

def is_therapist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if session['user_type']== 'therapist':
                return f(*args, **kwargs)
            else:
                return render_template('index.html',msg='You are not authorized to access the page.')
        except Exception as e:
            return render_template('index.html',msg='You are not authorized to access the page.')
    return wrap


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if session['user_type']== 'admin':
                return f(*args, **kwargs)
            else:
                return render_template('index.html',msg='You are not authorized to access the page.')

        except Exception as e:
            return render_template('index.html',msg='You are not authorized to access the page.')
    return wrap

def if_userprofile_notfound(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if pendingusref.child(session['user_id']).get() != None:
                return f(*args, **kwargs)
            else:
                return redirect('/user/profile')
        except Exception as e:
            print(str(e))
            return render_template('index.html',msg='You are not authorized to access the page.')
    return wrap

def if_therapistprofile_notfound(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if pendingtref.child(session['user_id']).get() != None:
                return f(*args, **kwargs)
            else:
                return redirect('/therapist/profile')
        except Exception as e:
            return render_template('index.html',msg='You are not authorized to access the page.')
    return wrap

def update_meetings(uid):
    try:
        if session['user_type']=='user':
            meetings = mref.order_by_child('UserID').equal_to(uid).get()
        else:
            meetings = mref.order_by_child('TherapistID').equal_to(uid).get()

        for meetid,meet in meetings.items():
            current_time = datetime.now(IST).replace(tzinfo=None)
            meet_time = datetime.strptime(meet['Date']+' '+meet['Time'],"%d/%m/%Y %I:%M %p")
            diff = ((current_time - meet_time).total_seconds())/60
            if diff > int(meet['SessionTime']):
                pmref.child(meetid).set(meet)
                mref.child(meetid).delete()
    except:
        pass


def notification(title,message,uid):
    current = datetime.now(IST)
    post_time = current.strftime('%d %m %Y %I:%M %p')
    nid = 'n'+ current.strftime('%Y%m%d%H%M%S')
    notification = {
        'Title':title,
        'Message': message,
        'Post-Time':post_time,
    }
    nref.child(uid).update({nid:notification})
