from flask import Blueprint, render_template, request, session, redirect
from firebaseref.firebasereference import *
from firebaseref.anonymousfunctions import *
from datetime import *

Therapist = Blueprint("Therapist", __name__, static_folder="static", template_folder="templates", static_url_path='/%s' % __name__)


@Therapist.route('/', methods=['GET', 'POST'])
def therapist():
    return render_template('index.html')


@Therapist.route('/createprofile', methods=['GET', 'POST'])
@is_therapist
@if_therapistprofile_notfound
def createtherapistprofile():

    if request.method == 'POST':

        tid = session['user_id']
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        days = request.form.getlist('days')
        start_pref = request.form.get('start-pref')
        end_pref = request.form.get('end-pref')
        highest_qualification = request.form.get('qualification')
        degree_college = request.form.get('degree-college')
        experience = request.form.get('experience')
        mob = request.form.get('mobile')
        nick = 'Dr. ' + fname

        file_contents = {
            "Firstname": fname,
            "Lastname": lname,
            "Nickname": nick,
            "Date of Birth": dob,
            "Gender": gender,
            "Preferred-days": days,
            "Preferred-time": {"Start-time": start_pref, "End-time": end_pref},
            "Qualification Details": {"Degree-college": degree_college, "Experience": experience, "Highest-degree": highest_qualification},
            "Contact": mob
        }

        try:
            tref.child(tid).update(file_contents)
            pendingusref.child(tid).delete()
            session['logged_in'] = True
            session['nickname'] = nick
            return redirect('/')
        except Exception as e:
            print(str(e))
            return render_template('create-therapistprofile.html', msg="An Error occurred! Profile not created. Please try again...")

    return render_template('create-therapistprofile.html', msg="Please Create Profile!")


@Therapist.route('/profile', methods=['GET', 'POST'])
@is_logged_in
@is_therapist
def therapistprofile():

    if request.method == 'POST':

        _id = session['user_id']
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        gender = request.form.get('gender')
        days = request.form.getlist('days')
        start_pref = request.form.get('start-pref')
        end_pref = request.form.get('end-pref')
        highest_qualification = request.form.get('qualification')
        degree_college = request.form.get('degree-college')
        experience = request.form.get('experience')
        mob = request.form.get('mobile')

        file_contents = {
            "Firstname": fname,
            "Lastname": lname,
            "Gender": gender,
            "Preferred-time": {"Start-time": start_pref, "End-time": end_pref},
            "Preferred-days": days,
            "Qualification Details": {"Degree-college": degree_college, "Experience": experience, "Highest-degreee": highest_qualification},
            "Contact": mob
        }

        try:
            tref.child(_id).update(file_contents)
        except Exception as e:
            print(str(e))

    _id = session['user_id']

    try:
        session['notifications'] = dict(list(nref.child(session['user_id']).get().items())[::-1])
    except:
        session['notifications'] = None

    try:
        stories = slpref.child(session["user_id"]).child('Stories-Posted').get() or {}
    except Exception as e:
        print(str(e))
        stories={}
    
    patient_details = {}
    
    try:
        past_meetings = list(pmref.order_by_child('TherapistID').equal_to(_id).get().values())
        # past_meetings.sort(key=lambda m: datetime.strptime(m['Date']+" "+m['Time'],"%d/%m/%Y %I:%M %p"))

        patient_ids = pyre_db.child('Therapists').child(_id).child('Patients').shallow().get().val()

        for pid in patient_ids:
            patient = [meet for meet in past_meetings if meet['UserID'] == pid]
            if len(patient) != 0:
                patient_details[pid] = patient

    except Exception as e:
        patient_details = {}
        print(str(e))

    data = tref.child(session['user_id']).get()
    blob = bucket.blob('Avatars/'+session['user_id'])
    if blob.exists():
        data['Avatar'] = blob.generate_signed_url(timedelta(seconds=300), method='get')

    return render_template('therapistprofile.html', data=data,  stories=stories, patient_details=patient_details)

@Therapist.route('/getmeetings', methods = ['POST','GET'])
def getmeetings():
    meetings = {}
    try:
        meetings = mref.order_by_child('TherapistID').equal_to(session['user_id']).get()
        meetings = dict(sorted(meetings.items(),key=lambda m: datetime.strptime(m[1]['Date']+" "+m[1]['Time'],"%d/%m/%Y %I:%M %p")))
    except Exception as e:
        print(str(e))
    return meetings

@Therapist.route('/deletenotification', methods=['POST', 'GET'])
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


@Therapist.route('/upload_avatar', methods=['POST', 'GET'])
def upload_avatar():
    if request.method == 'POST':
        img = request.files['img_file']
        img_extension = img.filename.split('.')[-1]
        blob = bucket.blob('Avatars/'+session['user_id'])
        blob.upload_from_file(img, content_type="image/"+img_extension.lower())
        return "Successful"
    else:
        return "Error"


@Therapist.route('/remove_avatar', methods=['POST', 'GET'])
def remove_avatar():
    try:
        blob = bucket.blob('Avatars/'+session['user_id'])
        blob.delete()
        return "Successful"
    except Exception as e:
        print(str(e))
        return "Error"
