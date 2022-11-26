from flask import Blueprint, render_template, url_for, request, session, redirect, json
from firebaseref.firebasereference import *
from firebaseref.anonymousfunctions import *
from datetime import *
from math import floor
import razorpay
import pytz

IST = pytz.timezone('Asia/Kolkata')
client = razorpay.Client(auth=("rzp_test_8paloDZIStBTAV", "X3YqtilHxaNssu9MSrOlWxsu"))

Appointments = Blueprint("Appointments", __name__, static_folder="static",
                         template_folder="templates", static_url_path='/%s' % __name__)

@Appointments.route('/appointments', methods=['POST', 'GET'])
@is_logged_in

def appointments():

    uid = session['user_id']

    if session['user_type'] == 'user':

        if request.method == "POST":

            total_meets = len(mref.order_by_child('UserID').equal_to(uid).get())
            if total_meets >= 2:
                return redirect('Appointments.appointments',msg='You already have 2 booked meetings.')

            if 'thirty' in request.form:
                tid = request.form['therapist30']
                time = request.form['time30']
                date = request.form['date30']
                calltype = request.form['calltype']
                mid = generate_id('m')
                tname = tref.child(tid).child('Nickname').get()

                contents = {
                    'UserID': uid,
                    'TherapistID': tid,
                    'TherapistName': tname,
                    'UserNickname': session['nickname'],
                    'Time': time,
                    'Date': date,
                    'RoomID': mid,
                    'Type':calltype,
                    'SessionTime':'30',
                    'Rescheduled':'False'
                }
                tmref.child(mid).set(contents)

                if session['email'][-12:] == '@somaiya.edu':
                    return redirect(url_for('Appointments.confirmbookingforcampus',mid=mid))

                if calltype == 'Audio':
                    msg = '30 Minutes Audio Session'
                    order = client.order.create(dict(amount=149*100, currency='INR', receipt=mid))
                    utransref.child(uid).child(mid).update({'razorpay_order_id':order['id'],'Verified':'False'})
                    return render_template('payment.html', msg=msg, mid=mid, amount=order['amount'], orderid=order['id'])
                elif calltype == 'Video':
                    msg = '30 Minutes Video Session'
                    order = client.order.create(dict(amount=249*100, currency='INR', receipt=mid))
                    utransref.child(uid).child(mid).update({'razorpay_order_id':order['id'],'Verified':'False'})
                    return render_template('payment.html', msg=msg, mid=mid, amount=order['amount'], orderid=order['id'])

            if 'sixty' in request.form:
                tid = request.form['therapist60']
                time = request.form['time60']
                date = request.form['date60']
                calltype = request.form['calltype']
                mid = generate_id('m')
                tname = tref.child(tid).child('Nickname').get()

                contents = {
                    'UserID': uid,
                    'TherapistID': tid,
                    'TherapistName': tname,
                    'UserNickname': session['nickname'],
                    'Time': time,
                    'Date': date,
                    'RoomID': mid,
                    'Type':calltype,
                    'SessionTime':'60',
                    'Rescheduled':'False'
                }
                tmref.child(mid).set(contents)

                if session['email'][-12:] == '@somaiya.edu':
                    return redirect(url_for('Appointments.confirmbookingforcampus',mid=mid))
                    
                if calltype == 'Audio':
                    msg = '60 Minutes Audio Session'
                    order = client.order.create(dict(amount=199*100, currency='INR', receipt=mid))
                    utransref.child(uid).child(mid).update({'razorpay_order_id':order['id'],'Verified':'False'})
                    return render_template('payment.html', msg=msg, mid=mid, amount=order['amount'], orderid=order['id'])
                elif calltype == 'Video':
                    msg = '60 Minutes Video Session'
                    order = client.order.create(dict(amount=399*100, currency='INR', receipt=mid))
                    utransref.child(uid).child(mid).update({'razorpay_order_id':order['id'],'Verified':'False'})
                    return render_template('payment.html', msg=msg, mid=mid, amount=order['amount'], orderid=order['id'])

        if utref.child(uid).get() == None:

            try:
                tids = pyre_db.child('Therapists').shallow().get().val()
                therapists = {tid: tref.child(tid).child('Nickname').get() for tid in tids}

            except Exception as e:
                therapists = {}
                print(str(e))

            return render_template('appointments.html', meetings=None, therapists=therapists, minDate='1d',msg='')

        else:

            therapists = {}
            tid = utref.child(uid).get()
            therapists[tid] = tref.child(tid).child('Nickname').get()

            try:
                update_meetings(session['user_id'])
            except Exception as e:
                print(str(e))

            try:
                meetings = mref.order_by_child('UserID').equal_to(uid).get().items()
                meetings = sorted(meetings,key=lambda m: datetime.strptime(m[1]['Date']+" "+m[1]['Time'],"%d/%m/%Y %I:%M %p"))
                current_time = datetime.now(IST).replace(tzinfo=None)

                for meetid,meet in meetings:
                    meet_time = datetime.strptime(meet['Date'] + ' ' + meet['Time'], '%d/%m/%Y %I:%M %p')
                    difference = ((meet_time - current_time).total_seconds())/60
                    if difference < 15:
                        meet['JB_enabled'] = True
                    else:
                        meet['JB_enabled'] = False
                    if difference < 180 or meet['Rescheduled']=='True':
                        meet['RS_enabled'] = False
                    else:
                        meet['RS_enabled'] = True

                past_meetings = list(pmref.order_by_child('UserID').equal_to(uid).get().values())
                past_meetings.sort(key=lambda m: datetime.strptime(m['Date']+" "+m['Time'],"%d/%m/%Y %I:%M %p"))

                try:
                    latest_meet_time = datetime.strptime(meetings[-1][1]['Date']+' '+meetings[-1][1]['Time'], '%d/%m/%Y %I:%M %p')
                except:
                    latest_meet_time = datetime.strptime(past_meetings[-1]['Date']+' '+past_meetings[-1]['Time'], '%d/%m/%Y %I:%M %p')

                days = ((current_time-latest_meet_time).total_seconds())/86400
                if days > 7:
                    minDate = '1d'
                elif days < 0:
                    minDate = str(7+abs(floor(days)))+'d'
                else:
                    minDate = str(7-int(days))+'d'

            except Exception as e:
                meetings = None
                minDate = '1d'
                print(str(e))

            msg=request.args.get('msg')
            if not msg:
                msg=''
            return render_template('appointments.html', meetings=meetings, therapists=therapists, minDate=minDate, msg=msg)

    elif session['user_type'] == 'therapist':

        try:
            update_meetings(session['user_id'])
            meetings = mref.order_by_child('TherapistID').equal_to(uid).get().items()
            meetings = sorted(meetings, key=lambda m: datetime.strptime(m[1]['Date']+" "+m[1]['Time'],"%d/%m/%Y %I:%M %p"))

            current_time = datetime.now(IST).replace(tzinfo=None)

            for meetid, meet in meetings:
                meet_time = datetime.strptime(
                    meet['Date'] + ' ' + meet['Time'], '%d/%m/%Y %I:%M %p')
                difference = ((meet_time - current_time).total_seconds())/60
                if difference < 15:
                    meet['JB_enabled'] = True
                else:
                    meet['JB_enabled'] = False

        except Exception as e:
            meetings = None
            print(str(e))

        return render_template('appointments.html', meetings=meetings, therapists=None, minDate='1d')

    else:
        return render_template('/')

#---------------------------------------- Get Availablity of Therapist ----------------------------------------#


@Appointments.route('/get_available_days', methods=['POST', 'GET'])
def get_available_days():
    if request.method == 'POST':
        tid = request.form['tid']
        data = (tref.child(tid).get())['Preferred-days']
        return json.dumps(data)


@Appointments.route('/get_available_slots', methods=['POST', 'GET'])
def get_available_slots():
    if request.method == 'POST':
        date = request.form['date']
        tid = request.form['tid']
        slots = {'not-available': []}
        slots['preferred'] = (tref.child(tid).get())['Preferred-time']
        slots['preferred']['End-time'] = (datetime.strptime(
            slots['preferred']['End-time'], '%I:%M %p') - timedelta(minutes=30)).strftime('%I:%M %p')

        try:
            meets = mref.order_by_child('TherapistID').equal_to(tid).get().values()
            for m in meets:
                if m['Date'] == date:
                    a = m['Time']
                    b = (datetime.strptime(a, '%I:%M %p') +
                         timedelta(minutes=int(m['SessionTime']))).strftime('%I:%M %p')
                    slots['not-available'].append([a, b])
        except Exception as e:
            print(str(e))
        return json.dumps(slots)

@Appointments.route('/rescheduleappointment', methods=['POST', 'GET'])
@is_logged_in
def rescheduleappointment():
    if request.method == 'POST':
        tid = request.form['tidRS']
        mid = request.form['midRS']
        dateRS = request.form['dateRS']
        timeRS = request.form['timeRS']
        print(tid,mid,date,time)
        try:
            data=mref.child(mid).get()
            mref.child(mid).child('Time').set(timeRS)
            mref.child(mid).child('Date').set(dateRS)
            mref.child(mid).child('Rescheduled').set('True')
            msg_u = ('You successfully rescheduled your session with therapist {0}. '+\
                    'Previous schedule: {1} {2}, New schedule: {3} {4}').format(data['TherapistName'],data['Date'],data['Time'],dateRS,timeRS)
            msg_t = ('Your session with user {0} has been rescheduled. '+\
                    'Previous schedule: {1} {2}, New schedule: {3} {4}').format(data['UserNickname'],data['Date'],data['Time'],dateRS,timeRS)
            notification('Session Successfully Rescheduled',msg_u,data['UserID'])
            notification('An appointment has been rescheduled!',msg_t,data['TherapistID'])
            return redirect('/appointments?msg=Your session has been rescheduled!')
        except Exception as e:
            print(str(e))
            return redirect('/appointments?msg=Error in rescheduling your session! Contact us or report the issue.')


@is_logged_in
@Appointments.route('/verifytransaction', methods=['POST', 'GET'])
def verifytransaction():
    if request.method == 'POST':
        try:
            uid=session['user_id']
            mid=request.form['mid']
            data = {
              "razorpay_payment_id": request.form['razorpay_payment_id'],
              "razorpay_order_id": utransref.child(uid).child(mid).child('razorpay_order_id').get(),
              "razorpay_signature": request.form['razorpay_signature']
            }
            client.utility.verify_payment_signature(data)
            data['Verified']='True'
            transref.child(uid).child(mid).update(data)
            utransref.child(uid).child(mid).child('Verified').set('True')
            return redirect(url_for('Appointments.confirmbooking',mid=mid))
        except Exception as e:
            print(str(e))
            return render_template('index.html',msg='Error in verifying transaction. If money has been deducted please wait for refund.')
    return redirect('/')

@Appointments.route('/confirmbooking', methods=['POST', 'GET'])
@is_logged_in
def confirmbooking():
    try:
        mid=request.args.get('mid')
        data = tmref.child(mid).get()
        uid=data['UserID']
        tid=data['TherapistID']
        if str(utransref.child(uid).child(mid).child('Verified').get()) != 'True':
            raise Exception
        mref.child(mid).set(data)
        uref.child(uid).child('Meetings').set({mid:data['Type']})
        tref.child(tid).child('Meetings').set({mid:data['Type']})
        utref.child(uid).set(tid)
        tref.child(tid).child('Patients').update({uid:data['UserNickname']})
        utransref.child(uid).child(mid).delete()
        msg_u = ("You have successfully scheduled your {0} min {1} session with therapist '{2}'"+
                 " on {3} at {4}. You can join the session through appointments section on"+
                 " respective date and time. Make sure you read the terms and conditions."+
                 " Happy Counselling!").format(data["SessionTime"],data["Type"],data["TherapistName"],data["Date"],data["Time"])
        msg_t = ("You have an upcoming {0} min {1} session with client '{2}' on {3} at {4}."+
                 " You can join the session through appointments section on respective date and time."+
                 " Happy Counselling!").format(data["SessionTime"],data["Type"],data["UserNickname"],data["Date"],data["Time"])
        notification('Session Successfully Booked!',msg_u,uid)
        notification('An appointment is scheduled!',msg_t,tid)
        tmref.child(mid).delete()
        return redirect(url_for('Appointments.appointments',msg='Your session has been booked!'))
    except Exception as e:
        print(str(e))
        return redirect(url_for('Appointments.appointments',msg='Error in confirming your slot.\\nIf amount has been deducted from your account.\\nPlease wait for refund.',time='10000'))
    


@Appointments.route('/confirmbookingforcampus', methods=['POST', 'GET'])
@is_logged_in
def confirmbookingforcampus():
    try:
        mid=request.args.get('mid')
        data = tmref.child(mid).get()
        uid=data['UserID']
        tid=data['TherapistID']
        mref.child(mid).set(data)
        uref.child(uid).child('Meetings').set({mid:data['Type']})
        tref.child(tid).child('Meetings').set({mid:data['Type']})
        utref.child(uid).set(tid)
        tref.child(tid).child('Patients').update({uid:data['UserNickname']})
        utransref.child(uid).child(mid).delete()
        msg_u = ("You have successfully scheduled your {0} min {1} session with therapist '{2}'"+
                 " on {3} at {4}. You can join the session through appointments section on"+
                 " respective date and time. Make sure you read the terms and conditions."+
                 " Happy Counselling!").format(data["SessionTime"],data["Type"],data["TherapistName"],data["Date"],data["Time"])
        msg_t = ("You have an upcoming {0} min {1} session with client '{2}' on {3} at {4}."+
                 " You can join the session through appointments section on respective date and time."+
                 " Happy Counselling!").format(data["SessionTime"],data["Type"],data["UserNickname"],data["Date"],data["Time"])
        notification('Session Successfully Booked!',msg_u,uid)
        notification('An appointment is scheduled!',msg_t,tid)
        tmref.child(mid).delete()
        return redirect(url_for('Appointments.appointments',msg='Your session has been booked!'))
    except Exception as e:
        print(str(e))
        return redirect(url_for('Appointments.appointments',msg='Error in confirming your slot.\\nIf amount has been deducted from your account.\\nPlease wait for refund.',time='10000'))