from flask import Blueprint, render_template, url_for, request, session, redirect, json
from firebaseref.firebasereference import *
from firebaseref.anonymousfunctions import *
from datetime import *
import threading
import pytz

IST = pytz.timezone('Asia/Kolkata')

Stories = Blueprint("Stories", __name__, static_folder="static", template_folder="templates", static_url_path='/%s' % __name__)

all_stories=[]
def load_all_stories():
    try:
        global all_stories
        allstories = list(pyre_db.child('Stories').shallow().get().val())
        allstories.sort(reverse=True)
        all_stories = allstories
    except:
        pass

@Stories.route('/stories', methods = ['POST','GET'])
def stories():
    msg=''
    if request.method == "POST":
        try:
            storytitle = request.form.get('storytitle')
            storybody = request.form.get('storybody')
            current = datetime.now(IST)
            post_time = current.strftime("%d %b %Y %I:%M %p")
            uid = session['user_id']
            sid = 's'+current.strftime("%Y%m%d%H%M%S")+uid[-1:-6:-1]

            contents =  { 'UID':uid,
                          'Nickname':session['nickname'],
                          'Title':storytitle,
                          'Body':  storybody.strip(),
                          'Likes':0,
                          'Comment-count':0,
                          'Post-Time':post_time,
                        }
            
            sarchiveref.child(sid).set(contents)
            msg='Your story will be posted once it gets approved.\\nCheck notifications for updates.'
        except Exception as e:
            print(str(e))
            pass

    try:
        stories = dict(list(sref.order_by_key().limit_to_last(10).get().items())[::-1])
        session['pagination-stories'] = len(stories)
    except:
        session['pagination-stories'] = 0
        stories = None

    try:
        threading.Thread(target=load_all_stories).start()
    except:
        pass

    try:
        for x in slpref.child(session['user_id']).child('StoriesLiked').get():
            try:
                stories[x]['liked']=True
            except:
                pass
    except Exception as e:
        print(str(e))

    return render_template('stories.html', stories=stories, msg=msg)

@Stories.route('/likestory', methods = ['POST','GET'])
@is_logged_in
def likestory():
    try:
        if request.method == "POST":
            storyid = request.form['storyid']
            increment = int(request.form['increment'])
            likes=int(sref.child(storyid).child('Likes').get()) + increment 
            if increment > 0:
                sref.child(storyid).child('Likes').set(likes)
                slpref.child(session['user_id']).child('StoriesLiked').update({storyid:'liked'}) 
            else:
                sref.child(storyid).child('Likes').set(likes)
                slpref.child(session['user_id']).child('StoriesLiked').child(storyid).delete()
            return "Successful"
    except:
        return "Unsuccessful"

@Stories.route('/story', methods = ['POST','GET'])
@is_logged_in
def story():
    msg=''
    if request.method == "POST":
        uid = session['user_id']
        storyid = request.args.get('sid')
        commentbody = request.form['commentbody']
        current = datetime.now(IST)
        post_time = current.strftime("%d %b %Y %I:%M %p")
        cid = 'c'+ current.strftime("%Y%m%d%H%M%S")+uid[-1:-6:-1] 
        contents = {    'UID':uid,
                        'Post-Time':post_time,
                        'Comment-Body':commentbody,
                        'Nickname':session['nickname']
                    }
        commentarchiveref.child(storyid).child(cid).set(contents);
        msg='Your comment will be posted once it gets approved.\\nCheck notifications for updates.'

    storyid = request.args.get('sid')
    storydata = sref.child(storyid).get()

    if slpref.child(session['user_id']).child('StoriesLiked').child(storyid).get():
        storydata['liked']=True

    try:
        comments = dict(list(cref.child(storyid).order_by_key().limit_to_last(5).get().items())[::-1])
        session['pagination-comments'] = len(comments)
    except Exception as e:
        print(str(e))
        comments=None
        session['pagination-comments'] = 0

    return render_template('story.html',storydata=storydata, sid=storyid, comments=comments, msg=msg)

@Stories.route('/load_more_stories', methods = ['POST','GET'])
def load_more_stories():
    global all_stories
    more_stories = {}
    i = session['pagination-stories']
    try:
        liked_stories = list(pyre_db.child('Stories-LP').child(session['user_id']).child('StoriesLiked').shallow().get().val())
    except:
        liked_stories=[]
    try:
        k=0
        for x in all_stories[i:i+10]:
            more_stories[k] = {x:sref.child(x).get()}
            if x in liked_stories:
                more_stories[k][x]['liked']=True
                liked_stories.remove(x)
            k+=1
        session['pagination-stories'] += len(more_stories)
    except Exception as e:
        pass
    return json.dumps(more_stories)

@Stories.route('/load_more_comments', methods = ['POST','GET'])
def load_more_comments():
    if request.method == "POST":
        storyid = request.form['storyid']
    more_comments = {}
    try:
        all_comments = list(pyre_db.child('Comments').child(storyid).shallow().get().val())
        all_comments.sort(reverse=True)
    except Exception as e:
        all_comments = []
    i = session['pagination-comments']
    try:
        for x in all_comments[i:i+5]:
            more_comments[x] = cref.child(storyid).child(x).get()
        session['pagination-comments'] += len(more_comments)
    except Exception as e:
        pass
    return json.dumps(more_comments)
