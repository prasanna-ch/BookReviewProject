import os
from flask import Flask, session, render_template, redirect, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from create import app
import datetime
from sqlalchemy import or_, and_

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
<<<<<<< HEAD
        # print(request.form)

||||||| cf6deb6

=======
>>>>>>> project
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
                return render_template("home.html", email = session.get("email"))
            else:
                return render_template("Register.html", message="Incorrect password")
<<<<<<< HEAD
        else:
            return render_template("Register.html", message="Invalid email")
    else:
        if session.get("email") is None:
            return render_template('Register.html')
    return render_template("login.html")
||||||| cf6deb6
    return render_template("Register.html", message="Invalid email")
=======
        else:
            return render_template("Register.html", message="Invalid email")
    else:
        if session.get("email") is None:
            return render_template('Register.html')
    return render_template("home.html", email = session.get("email"))
>>>>>>> project

@app.route("/logout")
def logout():
    session.clear()
    return render_template("Register.html")

@app.route("/")
def index():
    if session.get("email") is None:
        return render_template('Register.html')
<<<<<<< HEAD
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
||||||| cf6deb6
    return render_template("login.html")
    
=======
    return render_template("home.html",email=session.get("email"))

@app.route("/login/books",methods = ["GET","POST"])
def books():
    if request.method == "GET":
        return render_template("login.html")
    else:
        tag = request.form.get("name")
        search = "%{}%".format(tag)
        books = Books.query.filter(or_(Books.isbn.ilike(search), Books.title.ilike(search), Books.author.ilike(search), Books.year.like(search)))
        return render_template("login.html",msg=books,status="searched",tag=tag)


@app.route("/api/search", methods=["POST"])
def searchAPI() :
    try :
        if (not request.is_json) :
            return jsonify({"error" : "Not a json request"}), 400
        requestData = request.get_json()
        if "search" not in requestData:
            return jsonify({"error" : "Missing search field"}), 400
        if "email" not in requestData :
            return jsonify({"error" : "Missing email field"}), 400
        value = requestData.get("search")
        if len(value) == 0 :
            return jsonify({"error" : "No results found"}), 404
        email = requestData.get("email")
        isEmail = Users.query.get(email)
        if isEmail is None :
            return jsonify({"error" : "Not a registered email"}), 200
        tag = "%{}%".format(value)
        books = Books.query.filter(or_(Books.isbn.ilike(tag), Books.title.ilike(tag), Books.author.ilike(tag), Books.year.like(tag)))
        try :
            books[0].isbn
            li = []
            for book in books :
                diction = {}
                diction["isbn"] = book.isbn
                diction["title"] = book.title
                diction["author"] = book.author
                diction["year"] = book.year
                li.append(diction)
            return jsonify({"books" : li}), 200
        except Exception as ex :
            return jsonify({"error" : "no results found"}), 404
    except Exception as e:
        return jsonify({"error" : "Server Error"}), 500

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
>>>>>>> project
