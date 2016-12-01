from flask import Flask, render_template,request,url_for,redirect


app=Flask(__name__)
users=[]
@app.route("/",methods=["GET"])
def home():         
    success=request.args.get('success')   
    return render_template("index.html",success=success,users=users,count=len(users))
@app.route("/<username>", methods=['POST','DELETE',"GET"])
def remove(username=None):
    users.remove(username)
    afterdelete="Record <strong><em>{}</em></strong> successfully deleted".format(username)
    redirect(url_for("home"))
    return render_template("index.html",users=users,after=afterdelete,count=len(users))
@app.route("/<username>/edit",methods=['POST','GET'])
def viewuser(username):
    error=""
    success="The record <strong><em>{}</strong></em> was successfully update".format(username)
    if request.method=="POST":
        newusername=request.form['username'].strip()
        if(newusername==""):
            error="Please give us a username"
        else:
            users[users.index(username)]=newusername
            return redirect(url_for('home',success=success))
    return render_template("view.html",user=username,error=error)
@app.route("/user/new",methods=["POST","GET"])
def newuser():
    error=None
    if request.method=="POST":
        if(request.form['username'].strip()==""):
            error="Please give us a username"
        else:
            users.append(request.form['username'])
            return redirect(url_for('home',success="The record was successfully saved"))
    return render_template('new_user.html',error=error)
if __name__ =="__main__":
    app.run(debug=True)

