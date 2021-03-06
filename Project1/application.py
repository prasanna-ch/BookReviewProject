import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from create import app
import datetime

app = Flask(__name__)
os.environ['DATABASE_URL'] =  'postgres://vnvllzmogbmndv:8296aad966c453ef11dc98457f1e3ff5ebf3f5ac6e8019508f2d42cc2fd7f517@ec2-52-70-15-120.compute-1.amazonaws.com:5432/ddm0vcg85hm9a8'
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
        # e=email(email)
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
        else:
            return render_template("Register.html", message="Invalid email")
    else:
        if session.get("email") is None:
            return render_template('Register.html')
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("Register.html")  

@app.route("/")
def index():
    if session.get("email") is None:
        return render_template('Register.html')
    return render_template("login.html")
@app.route("/login/books",methods = ["GET","POST"])
def books():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # searchitem=request.form.get("name")
        tag = request.form.get("name")
        search = "%{}%".format(tag)
        books1 = Books.query.filter(Books.title.ilike(search)).all()
        books2 = Books.query.filter(Books.isbn.ilike(search)).all()
        books3 = Books.query.filter(Books.author.ilike(search)).all()
        books4 = Books.query.filter(Books.year.ilike(search)).all()
        books=books1+books2+books3+books4



        # li = Users.query.filter(Users.email.like('%'+ searchitem +'%')).all()
        # print(posts)
        return render_template("login.html",msg=books,status="searched",tag=tag)
@app.route("/login/books/<isbn>", methods=["GET","POST"])
def book_detail(isbn):
    if request.method == "GET":
        book = Books.query.get(isbn)
        email=session.get('email')
        rev=db.query(Reviews).all()
        reviewlist={}
        for i in rev:
            if i.book_isbn == isbn and i.email!=email:
                l=[]
                name=i.email.split('@')[0]
                l.append(i.review)
                l.append(i.rating)
                reviewlist[name]=l
        print(reviewlist)
        for i in rev:
            if i.email == email and i.book_isbn == isbn:
                review=i.review
                rating=i.rating
                return render_template("book_details.html",msg="Already reviewed",review=review,book=book,rating=rating,rl=reviewlist)
        return render_template("book_details.html",msg="not reviewed",book=book,rl=reviewlist)
    else:
        print("here in post method")
        book = Books.query.get(isbn)
        isbn=book.isbn
        email=session.get('email')
        review=request.form.get("review")
        rating=request.form.get("star")
        print(rating)
        r=Reviews(email=email, book_isbn=isbn, review=review, rating=rating)
        db.add(r)
        db.commit()
        return render_template("book_details.html",msg="reviewed",review=review,book=book,rating=rating)


if __name__ == "__main__":
    app.run()