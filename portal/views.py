from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
import hashlib
import json
from datetime import datetime
#custom imports
from .models import Users
user_object = Users()
portal = Blueprint("portal", __name__, template_folder='../template', static_folder='../static',
                   static_url_path='../static')


@portal.errorhandler(404)
def page_not_found(error):
    return render_template('portal/404.html'), 404




@portal.route('/')
def index():
    print('called')
    return render_template('portal/home.html')


@portal.route('/profile')
def profile():
    user=user_object.get_user_profile()
    return render_template('portal/profile.html',user=user)


@portal.route('/signup', methods=['POST','GET'])
def signup():
    try:
        if request.method == 'POST':
            #x = request.get_json(force=True)
            email= request.form.get('email')
            user_type="Researcher"
            user={
                "_id":email,
                "email":email,
                "first_name":request.form.get('first_name'),
                "last_name":request.form.get('last_name'),
                "password":request.form.get('password'),
                "phone":request.form.get('phone'),
                "dob":request.form.get('dob'),
                "department":request.form.get('department'),
                "address":request.form.get('address'),
                "batch":"July 2020",
                "profile_picture":None,
                "twitter":None,
                "skype":None,
                "facebook":None,
                "github":None,
                "status":True,
                "user_type":user_type,
                "semesters":[]
            }
            print("this is user: ",user)
            registration_status = user_object.save_user(user,user_type)
            if registration_status == True:
                return redirect(url_for("portal.signin"))
            else:
                flash(registration_status)
                return render_template('portal/signup.html')
        else:
            return render_template('portal/signup.html')
    except Exception as error:
        print(error)
        return render_template('portal/signup.html')


@portal.route('/signin', methods = ['GET', 'POST'])
def signin():
    try:
        if request.method == 'POST':
            #x = request.get_json(force=True)
            email= request.form.get('email')
            password= request.form.get('password')
            
            login_status = user_object.login_user(email,password)
            if login_status==True:
                flash('Logged in successfully')
                return redirect(url_for("portal.index"))
            else:
                print("Here :",login_status)
                flash(login_status)
                return redirect(url_for('portal.index'))
        else:
            return redirect(url_for('portal.index'))
    except Exception as error:
        print(error)
        return redirect(url_for('portal.index'))


@portal.route('/logout', methods=['POST','GET'])
def logout():
    try:
        session['logged_in']=False
        session["username"] = None
        session["name"] = None
        session["user_type"] = None
        session['id'] = None
        return redirect(url_for('portal.signin'))
    except Exception as error:
        print(error)
        return redirect(url_for('portal.signin'))

