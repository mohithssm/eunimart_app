import hashlib, binascii, os

from flask import Flask, session, request, render_template, flash, redirect, jsonify, url_for
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from create import app
from datetime import timedelta

app.secret_key = "1c488f4b4a21cd7fbc5007664656985c2459b2362cf1f88d44b97e750b0c14b2cf7bc7b792d3f45db"
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/")
@app.route("/index")
def index() :
    return render_template("index.html")

@app.route("/register")
def register() :
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login() :

    if request.method == "GET" :
        if session.get("user_email") :
            return redirect(url_for("user"))
        else :
            return render_template("login.html")
    else :
        return render_template("login.html")

@app.route("/authenticate", methods=["GET", "POST"])
def authenticate() :

    if request.method == "POST" :

        emailID = request.form.get("emailID")
        user = User.query.filter_by(email=emailID).first()
        password = request.form.get("pwd")

        if user :

            salt = user.password[:64]
            stored_password = user.password[64:]

            pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')

            if stored_password == pwdhash :
                session["user_email"] = user.email
                session.permanent=True
                flash("Login Succesful !", "info")
                return redirect(url_for("user"))
            else :
                flash("Please create an Account", "info")
                return redirect(url_for('register'))
        else :
            flash("Please create an Account", "info")
            return redirect(url_for('register'))
    else :
        
        if  session.get("user_email") :
            flash("Already Logged in !", "info")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/logout")
def logout() :
    
    if session.get("user_email") :
        session.pop("user_email", None)
        flash("You have been Logged out !")
        return redirect(url_for("login"))
    else :
        flash("Please Login", "info")
        return redirect(url_for("login"))

@app.route("/profile", methods=["GET","POST"])
def profile() :

    if request.method == "GET" :

        return render_template("register.html")

    if request.method == "POST" :

        name = request.form.get("name")

        emailID = request.form.get("emailID")

        password = request.form.get("pwd")

        dateOfBirth = request.form.get("dob")
        
        gender = request.form["options"]
        
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash) 

        password = (salt + pwdhash).decode('ascii')  

        user = User(name=name, email=emailID, password=password, dateOfBirth=dateOfBirth, gender=gender)

        try :

            db.session.add(user)
            
            db.session.commit()

            return render_template("profile.html", name=name, email=emailID, dob=dateOfBirth, gender=gender)

        except Exception as exc:
            print(exc,"exception")
            flash("An Account with same Email id alresdy exists", "info")
            return redirect(url_for("register"))


@app.route("/user", methods=["GET", "POST"])
def user() :
    
    if session.get("user_email") :
        user_email = session["user_email"]
        user = User.query.get({"email":user_email})
        if user.role == 'Admin' :
            flash("You have logged in successfully..!!")
            return redirect(url_for('admin'))
        candidates = Candidate.query.all()
        return render_template("candidates.html", user=user_email, candidates = candidates)
    else :
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route('/voted', methods=["POST"])
def voted():
    # data = request.get_json()
    
    id = request.form.get('vote')
    print(id,'id')
    cand_data = Candidate.query.get(id)
    user_data = User.query.get({"email" : session.get('user_email')})
    print(user_data.voted, "voted")
    if user_data.voted == False:

        user_data.voted = True
        cand_data.Votes += 1
        db.session.add(user_data)
        db.session.add(cand_data)
        db.session.commit()
        flash("Voted Successfully..!!", "info")
        return redirect(url_for("logout"))
        # return jsonify({"success": True, "status":"200"})
    else:
        flash("You have already voted","info")
        flash("Logged out successfully..!!", "info")
        return redirect(url_for("logout"))

@app.route("/admin")
def admin() :
    if session.get("user_email") :
        candidates = Candidate.query.all()
        return render_template("admin.html", candidates=candidates)
    else :
        flash("Please Login First", "info")
        return redirect(url_for("/login"))

if __name__ == "__main__" :
    app.run(debug=True)

    # postgres://nduktukglegvct:5b98a81abcb2587aae61ad05ec1b46c5f989f989ccc7dec095486d2157d244ae@ec2-18-211-97-89.compute-1.amazonaws.com:5432/d1k7d9a860oaa3
