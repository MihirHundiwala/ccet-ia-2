from flask import Blueprint, render_template, request, session
from firebaseref.firebasereference import mref

Therapy = Blueprint("Therapy", __name__, static_folder="static", template_folder="templates", static_url_path='/%s' % __name__)

@Therapy.route('/therapy', methods=['GET', 'POST'])
def therapy():
	roomid = request.args.get('therapyid')
	meeting = list(mref.order_by_child('RoomID').equal_to(roomid).get().values())[0]
	if session['user_id'] == meeting['UserID'] or session['user_id'] == meeting['TherapistID']:
		return render_template('therapy.html',roomid=roomid)
	else:
		return 'Your Therapy ID doesnt exist.'