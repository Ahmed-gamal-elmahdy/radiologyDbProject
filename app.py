import os
import mysql.connector
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import random
from functools import wraps


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Query database for username then update all session info
def update_session():
        sql = "SELECT * FROM users WHERE username = %s"
        val=(session["name"],)
        mycursor.execute(sql,val)
        rows = mycursor.fetchall()
        session["id"] = rows[0][0]
        session["name"] = rows[0][1]
        session["email"] = rows[0][2]
        session["token"] = rows[0][4]
        session["type"] = rows[0][5]
        if session["type"] == "Staff":
            sql = "SELECT ID FROM staff WHERE uid = %s"
            val=(session["id"],)
            mycursor.execute(sql,val)
            rows = mycursor.fetchall()
            if(len(rows) == 0):
                session["empty"] = "yes"
            else:
                session["staffid"] = rows[0][0]
                session["empty"] = None

        if session["type"] == "Patient":
            sql = "SELECT ID FROM patients WHERE uid = %s"
            val=(session["id"],)
            mycursor.execute(sql,val)
            rows = mycursor.fetchall()
            if(len(rows) == 0):
                session["empty"] = "yes"
            else:
                session["patientid"] = rows[0][0]
                session["empty"] = None

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  db="final"
)
mycursor = mydb.cursor()
@app.route("/")
@login_required
def index():
    update_session()
    print(session)
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        sql = "SELECT * FROM users WHERE username = %s"
        val = (username,)
        mycursor.execute(sql,val)
        rows = mycursor.fetchall()  
        if (len(rows) != 0):
            return render_template("register.html",error="This Username is registered before")
        else:
            sql = "SELECT * FROM users WHERE email = %s"
            val = (email,)
            mycursor.execute(sql,val)
            rows = mycursor.fetchall()  
            if (len(rows) != 0):
                return render_template("register.html",error="This Email is registered before")
            else:
                try:
                    password = str(generate_password_hash(request.form.get("password")))
                    accountType = str(request.form.get("accountType"))
                    Token =  random.randint(1000,9999)
                    sql = "INSERT INTO USERS (Username,Email,Password,Token,Type) VALUES (%s, %s, %s, %s, %s)"
                    values = (username,email,password,Token,accountType)
                    mycursor.execute(sql, values)
                    mydb.commit()   
                    # Redirect user to home page
                    return redirect("/")
                except:
                    return render_template("register.html",error="Something Went wrong ")        
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = "SELECT * FROM users WHERE username = %s"
        val=(username,)
        mycursor.execute(sql,val)
        rows = mycursor.fetchall()
        if (len(rows) != 1):
            return render_template("login.html",error="Wrong Credentials")
        if check_password_hash(rows[0][3], password):
            session["id"] = rows[0][0]
            session["name"] = rows[0][1]
            session["email"] = rows[0][2]
            session["token"] = rows[0][4]
            session["type"] = rows[0][5]
        return redirect("/")
    else:
        return render_template("login.html")
@app.route("/addpatient",  methods=["GET", "POST"])
@login_required
def addpatient():
    if(not session["empty"]):
        return render_template("index.html",msg="already registered your info")
    else:
        if request.method == "POST":
            name=request.form.get("name")
            ssn=request.form.get("ssn")
            age=request.form.get("age")
            phone=request.form.get("phone")
            gender=request.form.get("gendertype")
            history=request.form.get("history")
            sql = "SELECT * FROM patients WHERE ssn = %s"
            val = (ssn,)
            mycursor.execute(sql,val)
            rows = mycursor.fetchall()  
            if (len(rows) != 0):
                return render_template("addpatient.html",error="This SSN is registered before")
            else:
                sql = "INSERT INTO patients (UID,Name,SSN,Age,Gender,History,Phone) VALUES (%s, %s, %s, %s, %s,%s ,%s)"
                values = (session["id"],name,ssn,age,gender,history,phone)
                mycursor.execute(sql, values)
                mydb.commit()
                return render_template("index.html",msg="Info saved successfully")
        else:
            return render_template("addpatient.html")
@app.route("/addstaff",  methods=["GET", "POST"])
@login_required
def addstaff():
    if(not session["empty"]):
        return render_template("index.html",msg="already registered your info")
    else:
        if request.method == "POST":
            name=request.form.get("name")
            ssn=request.form.get("ssn")
            age=request.form.get("age")
            job=request.form.get("job")
            gender=request.form.get("gendertype")
            schedule=request.form.get("schedule")
            sql = "SELECT * FROM staff WHERE ssn = %s"
            val = (ssn,)
            mycursor.execute(sql,val)
            rows = mycursor.fetchall()  
            if (len(rows) != 0):
                return render_template("addstaff.html",error="This SSN is registered before")
            else:
                sql = "INSERT INTO staff (UID,Name,SSN,Age,Gender,Schedule,Job) VALUES (%s, %s, %s, %s, %s,%s ,%s)"
                values = (session["id"],name,ssn,age,gender,schedule,job)
                mycursor.execute(sql, values)
                mydb.commit()
                update_session()
                return render_template("index.html",msg="Info saved successfully")
        else:
            return render_template("addstaff.html")
@app.route("/search", methods=["GET","POST"])
@login_required
def search():
    if request.method=="POST":
        accounttype=request.form.get("accounttype")
        searchtype=request.form.get("searchtype")
        q="'%"+request.form.get("q")+"%'"
        sql = "SELECT * FROM "+accounttype+" WHERE "+searchtype+" LIKE "+q
        mycursor.execute(sql)
        rows = mycursor.fetchall()
        length=len(rows)
        if(accounttype=="staff"):
            bol=True
        else:
            bol=False
        if(length==0):
            return render_template("search.html",error="No matched data")
        else:
            return render_template("search.html",rows=rows,isStaff=bol,len=length)
    else:
        return render_template("search.html")
@app.route("/complain", methods=["GET", "POST"])
def complain():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        problem=request.form.get("problem")
        details=request.form.get("details")
        date=datetime.now().date()
        time=datetime.now().time()
        sql= "INSERT INTO complaint (Name,Email,Problem,Details,Date,Time) VALUES (%s, %s, %s, %s, %s,%s)"
        values=(name,email,problem,details,date,time)
        mycursor.execute(sql, values)
        mydb.commit()
        return render_template("complain.html",msg="Complain had been submitted")

    else:
        return render_template("complain.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

#todo list:
# Scans, devices , appointments , admin cp , change pw , change username , reset password , change password,logs
            

        
