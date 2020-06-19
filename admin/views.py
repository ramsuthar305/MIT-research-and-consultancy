from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from flask import session
from datetime import datetime

#custom imports
from .models import Users, Shortlist
from .models import Jobs
from .models import *

shorlist_obj=Shortlist()
user_object = Users()
jobs=Jobs()
admin = Blueprint("admin", __name__, template_folder='../templates', static_folder='../static/admin',
                   static_url_path='../static/admin')

@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404

@admin.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        if session['logged_in']==True:
            return redirect(url_for("admin.dashboard"))
        if request.method == 'POST':
            print("check")
            username = request.form.get('username')
            password = request.form.get('password')
            if username == 'admin' and password == 'admin':
                session['logged_in']=True
                login_status = True
            if login_status==True:
                return redirect(url_for("admin.dashboard"))
            else:
                flash(login_status)
                return render_template('admin/admin_login.html', TOPIC_DICT = TOPIC_DICT)
        else:
            return render_template('admin/admin_login.html')
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/logout', methods=['POST','GET'])
def logout():
    try:
        session['logged_in']=False
        return redirect(url_for('admin.login'))
    except Exception as error:
        print(error)
        return redirect(url_for('admin.login'))


@admin.route('/',methods=['POST','GET'])
def dashboard():
    try:
        if session['logged_in']==True:
            return render_template('admin/dashboard.html')
        else:
            return redirect(url_for("admin.login"))
        
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/setbatch',methods=['POST','GET'])
def setbatch():
    try:
        if session['logged_in']==True:
            return render_template('admin/setbatch.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/setpages',methods=['POST','GET'])
def setpages():
    try:
        if session['logged_in']==True:
            return render_template('admin/setpages.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/approve',methods=['POST','GET'])
def approve():
    try:
        if session['logged_in']==True:
            return render_template('admin/approve.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/promote',methods=['POST','GET'])
def promote():
    try:
        if session['logged_in']==True:
            return render_template('admin/promote.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/notice',methods=['POST','GET'])
def notice():
    try:
        if session['logged_in']==True:
            return render_template('admin/notice.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/resources',methods=['POST','GET'])
def resources():
    try:
        if session['logged_in']==True:
            return render_template('admin/resources.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/register_supervisors',methods=['POST','GET'])
def register_supervisors():
    try:
        if session['logged_in']==True:
            return render_template('admin/register_supervisors.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/supervisors_registration',methods=['POST','GET'])
def supervisors_registration():
    supervisors_object = Supervisors()
    try:
        if request.method == 'POST':
            user_type = request.form.get('designation')
            email = request.form.get('email')

            for i in range(1,9):
                temp = "subdepartment" + str(i)
                subdept = request.form.get(temp)
                if len(subdept)>4:
                    break
                else:
                    subdept = "None"

            twitter = request.form.get('twitter')
            facebook = request.form.get('facebook')
            skype = request.form.get('skype')
            repos = request.form.get('repos')

            twitter = "None" if len(twitter)>0 else "None"
            facebook = "None" if len(twitter)>0 else "None"
            skype = "None" if len(twitter)>0 else "None"
            repos = "None" if len(twitter)>0 else "None"

            user={
                "_id":email,
                "email":email,
                "first_name":request.form.get('first_name'),
                "last_name":request.form.get('last_name'),
                "password":"123",
                "phone":request.form.get('phone'),
                "dob":request.form.get('dob'),
                "department":request.form.get('department'),
                "subdepartment":subdept,
                "address":request.form.get('address'),
                "gender":request.form.get('gender'),
                "nationality":request.form.get('nationality'),
                "profile_picture":None,
                "twitter":request.form.get('twitter'),
                "skype":request.form.get('skype'),
                "facebook":request.form.get('facebook'),
                "github":request.form.get('repos'),
                "status":True,
                "user_type":user_type
            }
            registration_status = supervisors_object.save_supervisor(user,user_type)
            flash('Registered Successfully')
            return redirect(url_for("admin.register_supervisors"))
        else:
            return render_template('admin/admin_login.html')
    except Exception as e:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/register_specialusers',methods=['POST','GET'])
def register_specialusers():
    try:
        if session['logged_in']==True:
            return render_template('admin/register_specialusers.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/specialusers_registration',methods=['POST','GET'])
def specialusers_registration():
    specialusers_object = SpecialUsers()
    try:
        if request.method == 'POST':
            user_type = "Special User"
            email = request.form.get('email')
            
            twitter = request.form.get('twitter')
            facebook = request.form.get('facebook')
            skype = request.form.get('skype')
            repos = request.form.get('repos')

            twitter = "None" if len(twitter)>0 else "None"
            facebook = "None" if len(twitter)>0 else "None"
            skype = "None" if len(twitter)>0 else "None"
            repos = "None" if len(twitter)>0 else "None"

            user={
                "_id":email,
                "email":email,
                "title":request.form.get('title'),
                "first_name":request.form.get('first_name'),
                "last_name":request.form.get('last_name'),
                "password":"123",
                "phone":request.form.get('phone'),
                "dob":request.form.get('dob'),
                "address":request.form.get('address'),
                "gender":request.form.get('gender'),
                "nationality":request.form.get('nationality'),
                "profile_picture":None,
                "twitter":request.form.get('twitter'),
                "skype":request.form.get('skype'),
                "facebook":request.form.get('facebook'),
                "github":request.form.get('repos'),
                "info":request.form.get('info'),
                "status":True,
                "user_type":user_type
            }
            registration_status = specialusers_object.save_specialuser(user,user_type)
            flash('Registered Successfully')
            return redirect(url_for("admin.register_specialusers"))
        else:
            return render_template('admin/admin_login.html')
    except Exception as e:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/editusers',methods=['POST','GET'])
def editusers():
    try:
        if session['logged_in']==True:
            return render_template('admin/editusers.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/blockusers',methods=['POST','GET'])
def blockusers():
    try:
        if session['logged_in']==True:
            return render_template('admin/blockusers.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/removeusers',methods=['POST','GET'])
def removeusers():
    try:
        if session['logged_in']==True:
            return render_template('admin/removeusers.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_scholars',methods=['POST','GET'])
def view_scholars():
    try:
        if session['logged_in']==True:
            return render_template('admin/view_scholars.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_supervisors',methods=['POST','GET'])
def view_supervisors():
    try:
        if session['logged_in']==True:
            return render_template('admin/view_supervisors.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_cosupervisors',methods=['POST','GET'])
def view_cosupervisors():
    try:
        if session['logged_in']==True:
            return render_template('admin/view_cosupervisors.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_authorities',methods=['POST','GET'])
def view_authorities():
    try:
        if session['logged_in']==True:
            return render_template('admin/view_authorities.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')