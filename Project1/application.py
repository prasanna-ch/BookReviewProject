import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Users, db
from create import app
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/register", methods=["GET","POST"])
def register():
    msg = ""
    if (request.method=="POST"):
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        timestamp = datetime.datetime.now()
        # print(request.form)

        try:
            new_user = Users(email = name, password = pwd, timestamp = timestamp)
            if(name == '' or pwd == ''):
                msg = "Email or password could not be empty"
                return render_template("Register.html", message = msg)
            else:
                db.add(new_user)
                db.commit()
                msg = "Registration was completed. Please Login"
                return render_template("Register.html", message = msg)
        
        except:
            msg = "You already registered with this email id. Please Login"
            return render_template("Register.html", message = msg)
    else:
        return render_template("Register.html")
    
@app.route("/admin", methods=["GET"])
def admin():
    data = Users.query.all()
    return render_template('admin.html', data = data)

@app.route("/login", methods=['POST','GET'])
def authenticate():
    if request.method == 'POST':
        email = request.form.get("name")
        password = request.form.get("pwd")
        # print ("email: ",email,"password:" , password)
        data = Users.query.get(email)
        # print (data)
        if data != None:
            print(data)
            if password == data.password:
                session["email"] = email
                return render_template("login.html")
            else:
                return render_template("Register.html", message="Incorrect password")
    return render_template("Register.html", message="Invalid email")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("Register.html")  

@app.route("/")
def index():
    if session.get("email") is None:
        return render_template('Register.html')
    return render_template("login.html")
    