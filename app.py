from flask import Flask, render_template,request,url_for,redirect
from json import dumps
from models import *
from flask_moment import Moment
import datetime
import jsonify
from requests import Response as res
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
    return render_template("index.html",posts=Post.select().order_by(Post.date_posted.desc()),datenow=datetime.datetime.now() ,after=afterdelete,count=len(Post.select().order_by(Post.date_posted.desc())))
@app.route("/<postid>/edit",methods=['POST','GET'])
def editpost(postid):
    error=""
    success="The record was successfully updated"
    post=Post.get(Post.id==postid)
    if request.method=="POST":
        newtitle=request.form['title'].strip()
        newcontent=request.form['content'].strip()
        if(newtitle=="" or newcontent==""):
            error="Please provide a title and content before saving"
        else:
            post.title=newtitle
            post.content=newcontent
            post.date_posted=datetime.datetime.now()
            post.save()
            return redirect(url_for('home',success=success))
    return render_template("view.html",post=post,error=error)
@app.route("/user/new",methods=["POST","GET"])
def new_post():
    error=None
    if request.method=="POST":
        if(request.form['userid'].strip()=="" or request.form['title'].strip()=="" or request.form['content'].strip()==""):
            error="Please fill in all the fields "
        else:
            Post.create(user_id=request.form['userid'],title=request.form['title'],content=request.form['content'])
            return redirect(url_for('home',success="The record was successfully saved"))
    return render_template('new_post.html',error=error)
@app.route("/post/<int:postid>",methods=["GET"])
def view_post(postid):
    post=Post.get(Post.id==postid)
    user=User.get(User.id==post.user_id)
    print(post)
    return render_template("view_post.html",post=post,datenow=datetime.datetime.now(),user=user)
@app.route("/api/posts",methods=['GET'])
def api_posts():
    posts=Post.select().order_by(Post.date_posted.desc())
    return res.json(posts.title)
@app.errorhandler (404)
def not_found(error):
    return render_template('404.html'), 404
if __name__ =="__main__":
    app.run(debug=True)

