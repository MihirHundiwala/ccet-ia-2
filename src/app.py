import os
from flask import Flask, render_template, url_for, request, session, redirect, json, jsonify, flash
from flask_sslify import SSLify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from user.user import User
from therapist.therapist import Therapist
from stories.stories import Stories
from appointments.appointments import Appointments
from therapy.therapy import Therapy
from admin.admin import Admin
from facts.facts import Facts
from firebaseref.firebasereference import *
from firebaseref.anonymousfunctions import *

import sys
sys.dont_write_bytecode = True

app = Flask(__name__)
app.secret_key = "super secret key"
sslify = SSLify(app)

app.register_blueprint(User, url_prefix='/user')
app.register_blueprint(Therapist, url_prefix='/therapist')
app.register_blueprint(Admin, url_prefix='/admin')
app.register_blueprint(Stories)
app.register_blueprint(Appointments)
app.register_blueprint(Therapy)
app.register_blueprint(Facts)


@app.after_request
def add_header(r):

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def get_user_type(_id):
    if aref.child(_id).get() != None:
        return 'admin'
    if tref.child(_id).get() != None:
        return 'therapist'
    else:
        return 'user'


@app.route('/', methods=['GET', 'POST'])
def basic():
    try:
        msg = request.args.get('msg')
        session['notifications'] = dict(list(nref.child(session['user_id']).get().items())[::-1])
    except:
        session['notifications'] = None
    return render_template('index.html')


#---------------------------------------- Authentication ----------------------------------------#
@app.route('/auth', methods=['GET', 'POST'])
def Auth():
    email = None
    if request.method == 'POST':
        if 'signin' in request.form:
            email = request.form['email'].strip()
            password = request.form['psw']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                account_info = auth.get_account_info(user['idToken'])
                if not account_info['users'][0]['emailVerified']:
                    auth.send_email_verification(user['idToken'])
                    return render_template('index.html',msg=("Please complete email verification.\\n"+\
                                                       "Check your email to find the verification link.\\n"+\
                                                       "You can then log into T-Space."),time="10000")

                _id = user['localId']
                session['user_id'] = _id
                session['email'] = email

                user = pendingusref.child(_id).get()
                if user != None:
                    session['user_type'] = user
                    return redirect('/'+user+'/createprofile')

                else:
                    user_type = get_user_type(_id)
                    session['email'] = email
                    session['logged_in'] = True
                    session['user_type'] = user_type

                    session['nickname'] = refer[user_type].child(_id).child("Nickname").get()
                    try:
                        session['notifications'] = dict(list(nref.child(session['user_id']).get().items())[::-1])
                    except:
                        session['notifications'] = None
                    return redirect(request.referrer)

            except Exception as e:
                e = str(e)
                print(e)
                if 'INVALID_EMAIL' in e:
                    flash("Invalid Email.", 'signin')
                elif 'EMAIL_NOT_FOUND' in e:
                    flash("Email doesn't exist. Please Sign Up", 'signin')
                elif 'INVALID_PASSWORD' in e:
                    flash("Incorrect Password. Try again.", 'signin')
                elif 'TOO_MANY_ATTEMPTS_TRY_LATER' in e:
                    flash('Too many attempts. Try again later.', 'signin')
                    flash('You can restore it immediately by resetting your password.', 'signin')
                else:
                    flash('Encountered an error while signing up. Try again later or report the issue.', 'signin')
                    flash('Check if you have verified your email.', 'signin')
                return render_template('index.html', redirected='True', showmodal='#signinmodal')

        if 'signup' in request.form:
            email = request.form['email'].strip()
            password = request.form['psw']
            user_type = 'user'

            try:
                user = auth.create_user_with_email_and_password(email, password)
                auth.send_email_verification(user['idToken'])
                pendingusref.child(user['localId']).set('user')

                return render_template('index.html',msg="You have successfully created your account.\\n"+\
                                                  "To proceed further please complete email verification.\\n"+\
                                                  "Check your email to find the verification link.\\n"+\
                                                  "You can then log into T-Space",time="10000")

            except Exception as e:
                e = str(e)
                if 'EMAIL_EXISTS' in e:
                    flash('Email is already in use.', 'signup')
                elif 'EMAIL_INVALID' in e:
                    flash('Enter a valid email ID')
                else:
                    flash('Encountered an error while signing up.Try again or report the issue.', 'signup')
                return render_template('index.html', redirected='True', showmodal='#signupmodal')

        if 'therapistsignup' in request.form:
            email = request.form['email'].strip()
            tname = request.form['tname'].strip()
            tmob = request.form['mob']

            try:
                file_contents = {
                    "Email": email,
                    "Full Name": tname,
                    "MobileNo": tmob
                }
                pendingtref.push(file_contents)
                msg = 'Thank you for your application.\\nWe will notify you shortly.'
                return render_template('index.html', msg=msg)

            except Exception as e:
                e = str(e)
                flash('Encountered an error while signing up.Try again later or report the issue.', 'therapistsignup')
                return render_template('index.html', redirected='True', showmodal='#therapistsignupmodal')

    return render_template('index.html', redirected='False', showmodal='')


#---------------------------------------- Logout ----------------------------------------#
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect("/")
    
#---------------------------------------- Forgot Password --------------------------------#
@app.route("/forgotpassword", methods=['POST', 'GET'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form['email'].strip()
    try:
        auth.send_password_reset_email(email)
        return 'Check email for the link to reset password.'
    except Exception as e:
        if 'EMAIL_NOT_FOUND' in str(e):
            return 'Entered email id is not registered on T-Space.'
        elif 'EMAIL_INVALID' in str(e):
            return 'Invalid email id.'
        else:
            return 'Encountered an error. Try again later or report the issue.'

#---------------------------------------- Notifications ----------------------------------#
@app.route('/deletenotification', methods=['POST', 'GET'])
@is_logged_in
def deletenotification():
    try:
        if request.method == "POST":
            notificationid = request.form['notificationid']
            uid = session['user_id']
            nref.child(uid).child(notificationid).delete()
            session['notifications'] = nref.child(session['user_id']).get()
            return "Successful"
    except:
        return "Unsuccessful"


#---------------------------------------- About Us ----------------------------------------#
@app.route('/aboutus', methods=['POST', 'GET'])
def aboutus():
    return render_template('about-us.html')


#---------------------------------------- Terms and Conditions ----------------------------------------#
@app.route('/terms', methods=['POST', 'GET'])
def terms():
    return render_template('terms-conditions.html')

@app.route('/comingsoon', methods=['POST', 'GET'])
def comingsoon():
    return render_template('coming-soon.html')

#---------------------------------------- Video-Chat ----------------------------------------#
socketio = SocketIO(app)


@socketio.on('connect')
def connect(auth):
    pass


@socketio.on('join-room')
def on_join(roomid, userid):
    join_room(roomid)
    socketio.emit('user-connected', userid, to=roomid, include_self=False)


@socketio.on('disconnect')
def disconnect():
    socketio.emit('user-disconnected', include_self=False)


@socketio.on('hang-up')
def hangup(roomid, userid):
    socketio.emit('user-disconnected', userid, to=roomid, include_self=False)


@socketio.on('camera-turned-off')
def camera_turned_off(roomid, userid):
    socketio.emit('camera-turned-off', userid, to=roomid, include_self=False)


@socketio.on('camera-turned-on')
def camera_turned_on(roomid, userid):
    socketio.emit('camera-turned-on', userid, to=roomid, include_self=False)


@socketio.on('message-to-client')
def message_to_client(roomid, msgdata):
    socketio.emit('message-from-client', msgdata, to=roomid, include_self=False)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


#---------------------------------------- Main ----------------------------------------#
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    if(os.environ.get('PORT')):
        port = os.environ.get('PORT')
    else:
        port = 5000
    socketio.run(app, port=int(port), host='0.0.0.0')
    # socketio.run(app, debug=True)
