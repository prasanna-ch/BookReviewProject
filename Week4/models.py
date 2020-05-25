from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(120), primary_key = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    
    def __init__(self, email, password, timestamp) :
        self.email = email
        self.password = password
        self.timestamp = timestamp

    def __repr__(self):
        return self.email
class Books(db.Model):
    __tablename__="books"
    isbn=db.Column(db.String,primary_key=True)
    title=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    year=db.Column(db.String,nullable=False)
    
    

    def __init__(self,isbn,title,author,year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
    def get_book_details(self,isbn):
        b = Books.query.get(isbn)
        return b
class Reviews(db.Model):
    __tablename__="reviews"
    email = db.Column(db.String, db.ForeignKey('users.email'))
    book_isbn = db.Column(db.String, db.ForeignKey('books.isbn'))
    review = db.Column(db.String)
    rating = db.Column(db.String)
    __table_args__ = (db.PrimaryKeyConstraint('email', 'book_isbn'),)

    def __init__(self, email, book_isbn, review, rating):
        self.email = email
        self.book_isbn = book_isbn
        self.review = review
        self.rating = rating
