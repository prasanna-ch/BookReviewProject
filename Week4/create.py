import os

from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://vnvllzmogbmndv:8296aad966c453ef11dc98457f1e3ff5ebf3f5ac6e8019508f2d42cc2fd7f517@ec2-52-70-15-120.compute-1.amazonaws.com:5432/ddm0vcg85hm9a8'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()

