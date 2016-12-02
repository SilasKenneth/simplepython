from flask import Flask, render_template,request,url_for,redirect
from json import dumps
from models import *
from flask_moment import Moment
import datetime
app=Flask(__name__)
moment=Moment(app)
@app.route("/",methods=["GET"])
def home():
    posts=Post.select().order_by(Post.date_posted.desc())  
    users=User.select()        
    
    success=request.args.get('success')   
    return render_template("index.html",success=success,posts=posts,count=len(posts),users=len(users) ,datenow=datetime.datetime.now())
@app.route("/delete/<int:postid>", methods=['POST','DELETE',"GET"])
def remove(postid):
    post=Post.get(Post.id==postid)
    post.delete_instance()
    afterdelete="Post successfully deleted"
    redirect(url_for("home"))
    return render_template("index.html",posts=Post.select().order_by(Post.date_posted.desc()),after=afterdelete,count=len(Post.select().order_by(Post.date_posted.desc())))
@app.route("/<username>/edit",methods=['POST','GET'])
def edituser(username):
    error=""
    success="The record <strong><em>{}</strong></em> was successfully update".format(username)
    if username not in users:
                return render_template("404.html")
    if request.method=="POST":
        newusername=request.form['username'].strip()
        if(newusername==""):
            error="Please give us a username"
        else:
            if username not in users:
                return render_template("404.html")
            users[users.index(username)]=newusername
            return redirect(url_for('home',success=success))
    return render_template("view.html",user=username,error=error)
@app.route("/user/new",methods=["POST","GET"])
def newuser():
    error=None
    if request.method=="POST":
        if(request.form['userid'].strip()=="" or request.form['title'].strip()=="" or request.form['content'].strip()==""):
            error="Please fill in all the fields "
        else:
            Post.create(user_id=request.form['userid'],title=request.form['title'],content=request.form['content'])
            return redirect(url_for('home',success="The record was successfully saved"))
    return render_template('new_user.html',error=error)
@app.route("/post/<int:postid>",methods=["GET"])
def view_post(postid):
    post=Post.get(Post.id==postid)
    user=User.get(User.id==post.user_id)
    print(post)
    return render_template("view_post.html",post=post,datenow=datetime.datetime.now(),user=user)
@app.errorhandler (404)
def not_found(error):
    return render_template('404.html'), 404
if __name__ =="__main__":
    app.run(debug=True)

