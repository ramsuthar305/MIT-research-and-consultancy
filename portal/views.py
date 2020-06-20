from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
import hashlib
import json
from datetime import datetime
#custom imports
from .models import *

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
    exdata = Extract_Data()
    user = exdata.get_researcher()
    return render_template('portal/userprofile.html',user=user)

@portal.route('/signup')
def signup():
    active = ""
    exdata = Extract_Data()
    active=exdata.get_active_batch()
    print(active)
    supers = exdata.get_supervisors()
    cosupers = exdata.get_cosupervisors()
    
    return render_template('portal/signup.html',active=active,supers=supers,cosupers=cosupers)

@portal.route('/registration', methods=['POST','GET'])
def registration():
    exdata = Extract_Data()
    active=exdata.get_active_batch()
    try:
        if request.method == 'POST':
            #x = request.get_json(force=True)
            email= request.form.get('email')
            user_type="Research Scholar"
            user={
                "_id":email,
                "batch":active,
                "email":email,
                "first_name":request.form.get('first_name'),
                "last_name":request.form.get('last_name'),
                "password":"123",
                "phone":request.form.get('phone'),
                "dob":request.form.get('dob'),
                "department":request.form.get('department'),
                "address":request.form.get('address'),
                "gender":request.form.get('gender'),
                "nationality":request.form.get('nationality'),
                "profile_picture":None,
                "twitter":request.form.get('twitter'),
                "skype":request.form.get('skype'),
                "facebook":request.form.get('facebook'),
                "github":request.form.get('repos'),
                "supervisor":request.form.get('supervisor'),
                "cosupervisor":request.form.get('cosupervisor'),
                "status":"0",
                "user_type":user_type,
                "semesters":[]
            }
            print("this is user: ",user)
            registration_status = user_object.save_user(user,user_type)
            if registration_status == True:
                flash("Registration Successful. You will receive an email after your account is activated")
                return redirect(url_for("portal.signup"))
            else:
                flash(registration_status)
                return redirect('portal.signup')
        else:
            return redirect('portal.signup')
    except Exception as error:
        print(error)
        return render_template('portal.signup')


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


@portal.route('/supervisors_panel', methods=['POST','GET'])
def supervisors_panel():
    exdata = Extract_Data()
    user = exdata.get_researcher()
    try:
        if session['logged_in']==True:
            return render_template('portal/supervisors_panel.html')
        else:
            return redirect(url_for("portal.index"))
    except Exception as error:
        print(error)
        return render_template('portal/index.html')

