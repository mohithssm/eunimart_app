import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
os.environ["DATABASE_URL"] = "postgres://nduktukglegvct:5b98a81abcb2587aae61ad05ec1b46c5f989f989ccc7dec095486d2157d244ae@ec2-18-211-97-89.compute-1.amazonaws.com:5432/d1k7d9a860oaa3"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://nduktukglegvct:5b98a81abcb2587aae61ad05ec1b46c5f989f989ccc7dec095486d2157d244ae@ec2-18-211-97-89.compute-1.amazonaws.com:5432/d1k7d9a860oaa3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
