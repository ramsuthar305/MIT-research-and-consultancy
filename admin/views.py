from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from flask import session
from datetime import datetime

#custom imports
from .models import Users, Shortlist
from .models import Jobs
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

@admin.route('/register_authorities',methods=['POST','GET'])
def register_authorities():
    try:
        if session['logged_in']==True:
            return render_template('admin/register_authorities.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
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