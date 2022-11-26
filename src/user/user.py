from flask import Blueprint, render_template, request, session, redirect
from firebaseref.firebasereference import *
from firebaseref.anonymousfunctions import *
from datetime import *

User = Blueprint("User", __name__, static_folder="static", template_folder="templates", static_url_path='/%s' % __name__)

@User.route('/', methods=['GET', 'POST'])
def user():
    return render_template('index.html')

@User.route('/createprofile', methods=['GET', 'POST'])
@is_user
@if_userprofile_notfound
def createuserprofile():

    if request.method == 'POST':

        uid = session['user_id']
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        nkname = request.form.get('nickname')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        mob = request.form.get('mobile')

        file_contents = {
        "Firstname": fname,
        "Lastname" : lname,
        "Nickname": nkname,
        "Gender" : gender,
        "Date of Birth" : dob,
        "Contact" : mob
        }
    
        try:
            uref.child(uid).set(file_contents)
            pendingusref.child(uid).delete()
            session['logged_in'] = True
            session['nickname'] = nkname
            return redirect('/')
        except Exception as e:
            print(str(e))
            return render_template('create-userprofile.html', msg="An Error occurred! Profile not created. Please try again...")
        
    return render_template('create-userprofile.html')

@User.route('/profile', methods=['GET', 'POST'])
@is_logged_in
@is_user
def userprofile():

    if request.method == 'POST':

        uid=session['user_id']
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        gender = request.form.get('gender')
        mob = request.form.get('mobile')

        file_contents = {
        "Firstname": fname,
        "Lastname" : lname,
        "Gender" : gender,
        "Contact" : mob
        }
    
        try:
            uref.child(uid).update(file_contents)
        except Exception as e:
            print(str(e))
    
    try:
        session['notifications'] = dict(list(nref.child(session['user_id']).get().items())[::-1])
    except:
        session['notifications'] = None

    try:
        stories = slpref.child(session["user_id"]).child('Stories-Posted').get() or {}
    except Exception as e:
        print(str(e))
        stories={}

    data = uref.child(session['user_id']).get()

    try:
        update_meetings(session['user_id'])
        blob = bucket.blob('Avatars/'+session['user_id'])
        if blob.exists():
            data['Avatar'] = blob.generate_signed_url(timedelta(seconds=300),method='get')
    except Exception as e:
        print(str(e))

    return render_template('userprofile.html', data=data, stories=stories)

@User.route('/getmeetings', methods = ['POST','GET'])
def getmeetings():
    meetings = {}
    past_meetings = {}
    try:
        meetings = mref.order_by_child('UserID').equal_to(session['user_id']).get()
        meetings = dict(sorted(meetings.items(),key=lambda m: datetime.strptime(m[1]['Date']+" "+m[1]['Time'],"%d/%m/%Y %I:%M %p")))
        past_meetings = pmref.order_by_child('UserID').equal_to(session['user_id']).get()
        past_meetings = dict(sorted(past_meetings.items(),key=lambda m: datetime.strptime(m[1]['Date']+" "+m[1]['Time'],"%d/%m/%Y %I:%M %p")))
    except Exception as e:
        print(str(e))
    return {'m':meetings,'p':past_meetings}

@User.route('/deletenotification', methods = ['POST','GET'])
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


@User.route('/upload_avatar', methods = ['POST','GET'])
def upload_avatar():
    if request.method == 'POST':
        img = request.files['img_file']
        img_extension = img.filename.split('.')[-1]
        blob = bucket.blob('Avatars/'+session['user_id'])
        blob.upload_from_file(img,content_type="image/"+img_extension.lower())
        return "Successful"
    else:
        return "Error"

@User.route('/remove_avatar', methods = ['POST','GET'])
def remove_avatar():
    try:
        blob = bucket.blob('Avatars/'+session['user_id'])
        blob.delete()
        return "Successful"
    except Exception as e:
        print(str(e))
        return "Error"