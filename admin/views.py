from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from flask import session
from datetime import datetime
import os

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
    batch_object = Batch()
    display_list = {}
    active = ""
    year = datetime.now().year
    L = []
    for i in reversed(range(1,5)):
        temp = year-i
        L.append(temp)
    L.append(year)
    for i in range(1,5):
        temp = year+i
        L.append(temp)
    try:
        if session['logged_in']==True:
            batchlist = batch_object.get_batches()
            active = batch_object.get_active_batch()
            if batchlist:
                display_list = batchlist
                display_list1 = batchlist
            return render_template('admin/setbatch.html', display_list=display_list,active=active, year=L)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/addbatch',methods=['POST','GET'])
def addbatch():
    try:
        batch_object = Batch()

        if request.method=="POST":
            bmonth = request.form.get("bmonth")
            byear = request.form.get("byear")
            batch_name = bmonth+" "+str(byear)
            bjoin = bmonth+str(byear)
            data = {
            "batch_name":batch_name,
            "bmonth":bmonth,
            "byear":byear,
            "bjoin":bjoin,
            "start_date":request.form.get("start_date"),
            "end_date":request.form.get("end_date"),
            "status":"0",
            "expire":"0"
            }
            registration_status = batch_object.add_batch(data)
            flash('Batch Added Successfully')
            return redirect(url_for("admin.setbatch"))
        else:
            return render_template('admin/admin_login.html')
    except Exception as e:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/activatebatch',methods=['POST','GET'])
def activatebatch():
    try:
        batch_object = Batch()
        if request.method=="POST":
            data = request.form.get("batch_name")
            registration_status = batch_object.activate_batch(data)
            flash('Batch Activated Successfully')
            return redirect(url_for("admin.setbatch"))
        else:
            return render_template('admin/admin_login.html')
    except Exception as e:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/expirebatch',methods=['POST','GET'])
def expirebatch():
    batch_object = Batch()
    display_list = {}
    try:
        if session['logged_in']==True:
            batchlist = batch_object.get_batches()
            if batchlist:
                display_list1 = batchlist
            return render_template('admin/expirebatch.html', display_list1=display_list1)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/expire_batch',methods=['POST','GET'])
def expire_batch():
    try:
        batch_object = Batch()
        if request.method=="POST":
            data = request.form.get("batch_name")
            registration_status = batch_object.expire_batch(data)
            flash('Batch Expired Successfully')
            return redirect(url_for("admin.expirebatch"))
        else:
            return render_template('admin/admin_login.html')
    except Exception as e:
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
                "status":"0",
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
                "status":"0",
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





@admin.route('/add_resource',methods=['POST','GET'])
def add_resource():
    try:
        resource_object = Resource()

        if request.method=="POST":
            title = request.form.get("title")
            author = request.form.get("author")
            resouce_type = request.form.get("resource_type")

            f = request.files['file']
            filename = f.filename
            path = os.path.join(app.config['UPLOAD_FOLDER']+"resources",filename)
            main_path = path.split("static/")[1]
            print(main_path)
            f.save(path)
            
            data = {
            "title":title,
            "author":author,
            "resource_type":resouce_type,
            "pdf":main_path,
            "pdfname":filename

            }
            registration_status = resource_object.add_resource(data)
            flash('Resource Added Successfully')
            return redirect(url_for("admin.add_resource"))
        else:
            return render_template('admin/resources.html')
    except Exception as e:
        print(e)
        return render_template('admin/resources.html')