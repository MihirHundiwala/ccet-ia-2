from flask import render_template, Blueprint, request, json
from firebaseref.firebasereference import *
from firebaseref.anonymousfunctions import *

Admin = Blueprint("Admin", __name__, static_folder="static", template_folder="templates", static_url_path='/%s' % __name__)

@Admin.route('/profile', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def adminprofile():
	try:
		stories = sarchiveref.get()
		comments = commentarchiveref.get()
	except:
		stories = None
		comments = None
	return render_template('admin-view.html', stories=stories, comments=comments)

@Admin.route('/approvestory', methods = ['POST','GET'])
@is_logged_in
@is_admin
def approvestory():
    try:
        if request.method == "POST":
            storyid = request.form['storyid']
            story = sarchiveref.child(storyid).get()
            uid = story['UID']
            sref.child(storyid).update(story)
            slpref.child(uid).child('Stories-Posted').update({storyid:story['Title']})
            sarchiveref.child(storyid).delete()
            message = "Congrats, your story  '{0}'  has been approved and can now be seen by others!".format(story['Title'])
            notification('Story Approved!',message,uid)
            return "Successful"
    except:
        return "Unsuccessful"

@Admin.route('/disapprovestory', methods = ['POST','GET'])
@is_logged_in
@is_admin
def disapprovestory():
    try:
        if request.method == "POST":
            storyid = request.form['storyid']
            story = sarchiveref.child(storyid).get()
            uid = story['UID']
            sarchiveref.child(storyid).delete()
            message = "Sorry, your story  '{0}'  didn't comply with the terms and conditions of our platform and has been disapproved!".format(story['Title'])
            notification('Story Disapproved!',message,uid)
            return "Successful"
    except Exception as e:
        print(str(e))
        return "Unsuccessful"

@Admin.route('/approvecomment', methods = ['POST','GET'])
@is_logged_in
@is_admin
def approvecomment():
    try:
        if request.method == "POST":
            storyid = request.form['storyid']      
            cid = request.form['commentid']
            storytitle = sref.child(storyid).child('Title').get()
            comment = commentarchiveref.child(storyid).child(cid).get()
            uid=comment['UID']
            count = sref.child(storyid).child('Comment-count').get()

            cref.child(storyid).child(cid).set(comment)
            sref.child(storyid).child('Comment-count').set(count+1)
            slpref.child(uid).child('Comments-Posted').update({cid:storyid})
            
            commentarchiveref.child(storyid).child(cid).delete()
            message = "Your comment  '{0}'  on story  '{1}'  has been approved and posted!".format(comment['Comment-Body'],storytitle)
            notification('Comment Approved!',message,uid)
            return "Successful"
    except Exception as e:
        print(str(e))
        return "Unsuccessful"

@Admin.route('/disapprovecomment', methods = ['POST','GET'])
@is_logged_in
@is_admin
def disapprovecomment():
    try:
        if request.method == "POST":
            storyid = request.form['storyid']
            cid = request.form['commentid']
            comment = commentarchiveref.child(storyid).child(cid).get()
            storytitle = sref.child(storyid).child('Title').get()     
            commentarchiveref.child(storyid).child(cid).delete()
            message = "Sorry, your comment  '{0}'  on story  '{1}'  didn't comply with the terms and conditions of our platform and has been disapproved !".format(comment['Comment-Body'],storytitle)
            notification('Comment Disapproved!',message,userid_comment)
            return "Successful"
    except Exception as e:
        print(str(e))
        return "Unsuccessful"