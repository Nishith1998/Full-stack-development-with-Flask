from application import app, db
from flask import render_template
from flask import request
from flask import Response
from flask import json

courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/index")
def indexfun():
    return render_template("index.html", index_active = True)

@app.route("/login")
def loginfun():
    return render_template("login.html", login_active = True)

@app.route("/courses/")
@app.route("/courses/<term>")
def coursesfun(term="Spring 2019"):
    #print(courseData)
    return render_template("courses.html", courseData = courseData, courses_active = True, term = term)

@app.route("/register")
def registerfun():
    return render_template("register.html", register_active = True)


@app.route("/enrollment", methods = ["GET", "POST"]) # if dont put methods in parameter fine with GET but not with POST(method not allowed error)
def enrollmentfun():
    # get method
    # cid = request.args.get("courseID")
    # title = request.args.get("title")
    # term = request.args.get("term")
    
    # post method
    cid = request.form.get("courseID")
    title = request.form['title']  # title field must be present otherwise site will crash
    term = request.form.get("term")
    return render_template("enrollment.html", enrollment_active = True, data={"id": cid, "title": title, "term": term})

@app.route("/api/")
@app.route("/api/<index>")
def apifun(index=None):
    if(index == None):
        jdata = courseData
    else:
        jdata = courseData[int(index)]
    
    return Response(json.dumps(jdata), mimetype="application/json")

class User(db.Document):
    user_id     =   db.IntField(unique = True)
    first_name  =   db.StringField(max_length = 50)
    last_name   =   db.StringField(max_length = 50)
    email       =   db.StringField(max_length = 30)
    password    =   db.StringField(max_length = 30)

@app.route("/user")
def userfun():
    # User(user_id=1, first_name="nishith", last_name="goswami", email="abc@tmail.com", password="abc123" ).save()
    # User(user_id=2, first_name="goni", last_name="swami", email="yoman@tmail.com", password="abcxyz" ).save()

    users = User.objects.all()
    
    return render_template("user.html", users=users)

@app.route("/register_submit", methods = ["POST"])
def register_submitfun():
    uname = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    return render_template("register_submit.html", data = {"uname":uname, "email":email, "password":password})