from application import app, db
from flask import render_template, request, Response, json, redirect, flash, url_for
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/index")
def indexfun():
    return render_template("index.html", index_active = True)

@app.route("/login", methods = ["GET", "POST"])
def loginfun():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        email    = loginform.email.data
        password = loginform.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):#password == user.password:
            flash(f"{user.first_name}, You are sucessfully logged in", "success")
            return redirect("/index")
        else:
            flash("Sorry, problem occurred","danger")
    return render_template("login.html", titleH1 = "Login" ,loginform = loginform, login_active = True)

@app.route("/courses/")
@app.route("/courses/<term>")
def coursesfun(term="Spring 2019"):
    #print(courseData)
    return render_template("courses.html", courseData = courseData, courses_active = True, term = term)

@app.route("/register", methods=['POST','GET'])
def registerfun():

    registerform = RegisterForm()
    if registerform.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = registerform.email.data
        password    = registerform.password.data
        first_name  = registerform.first_name.data
        last_name   = registerform.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", registerform=registerform, register_active=True)


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

@app.route("/user")
def userfun():
    # User(user_id=1, first_name="nishith", last_name="goswami", email="abc@tmail.com", password="abc123" ).save()
    # User(user_id=2, first_name="goni", last_name="swami", email="yoman@tmail.com", password="abcxyz" ).save()

    users = User.objects.all()
    
    return render_template("user.html", users=users)

@app.route("/register_submit", methods = ["POST"])
def register_submitfun():
    uname = request.form.get("first_name")
    email = request.form.get("email")
    password = request.form.get("password")

    return render_template("register_submit.html", data = {"uname":uname, "email":email, "password":password})