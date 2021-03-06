from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from flask import session
from datetime import datetime
import os

#custom imports

from .models import *

admin = Blueprint("admin", __name__, template_folder='../templates', static_folder='../static/admin',
                   static_url_path='../static/admin')

@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404

@admin.route('/resetmitrcadmin', methods=['GET','POST'])
def resetmitrcadmin():
    try:
        u = Users()
        secret_pass = "M#T@R&C#D^^!N"
        if request.method == "POST":
            val = request.form.get('password')
            if val == secret_pass:
                u.reset_admin()
                flash("Admin Reset Successful")
                return render_template('admin/admin_reset.html',success = "True")
            else:
                flash("You don't have permissions")
                return render_template('admin/admin_reset.html',success = "False")
        return render_template('admin/admin_reset.html')
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        print("check1")
        if request.method=="POST":
            username = request.form.get('username')
            password = request.form.get('password')
            print(username)
            u = Users()
            stat = u.admin_login(username,password)
            if stat:
                flash("Login Successfull")
                return redirect(url_for('admin.dashboard'))
            else:
                flash("Incorrect Username or Password")
        print("check 2")
        print("check 4")
        return render_template('admin/admin_login.html')
    except Exception as error:
        return redirect(url_for('admin.login'))


@admin.route('/logout', methods=['POST','GET'])
def logout():
    try:
        session['logged_in']=False
        session.clear()
        return redirect(url_for('admin.login'))
    except Exception as error:
        print(error)
        return redirect(url_for('admin.login'))


@admin.route('/',methods=['POST','GET'])
def dashboard():
    try:
        if session['logged_in']==True and session['user_type'] == "admin":
            return render_template('admin/dashboard.html')
        else:
            return redirect(url_for("admin.login"))
        
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/adminresetpassword', methods=['GET','POST'])
def adminresetpassword():
    try:
        if session['logged_in']==True and session['user_type'] == "admin":
            if request.method=="POST":
                old_pass = request.form.get("old_pass")
                newpass1 = request.form.get("newpass1")
                newpass2 = request.form.get("newpass2")
                print(old_pass,newpass1,newpass2)
                u = Users()
                stat = u.check_old_pass(old_pass)
                if stat:
                    if newpass1==newpass2:
                        u.update_pass(newpass1)
                        flash("Password Changed Successfully")
                        return redirect(url_for('admin.dashboard'))
                    else:
                        flash("New Password and Confirm Password do not match")
                else:
                    flash("Old Password is Incorrect")
            return render_template('admin/admin_reset_password.html')
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template(url_for('admin.login'))

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

@admin.route('/approve',methods=['POST','GET'])
def approve():
    b = Batch()
    pending = b.fetch_pending()
    try:
        if session['logged_in']==True:
            return render_template('admin/approve.html',pending=pending)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/authorize',methods=['POST','GET'])
def authorize():
    b = Batch()
    pending = b.fetch_pending()
    try:
        if session['logged_in']==True:
            if request.method=="POST":
                userid = request.form.get('userid')
                if request.form['submitf']=="accept":
                    status = b.authorization(userid,"1")
                    flash("Account Activated Successfully")

                if request.form['submitf']=="reject":
                    status = b.authorization(userid,"2")
                    flash("Account Deleted Successfully")

                return redirect(url_for('admin.approve'))
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/promote',methods=['POST','GET'])
def promote():
    try:
        if session['logged_in']==True:
            u = UserEdits()
            users = ""
            batch = ""
            department = ""
            batch_object = Batch()
            batches = batch_object.get_batches()
            deplist = []
            departments = batch_object.get_departments()
            for i in departments:
                temp = {
                "depname":i,
                "djoin":i.replace(" ","")
                }
                deplist.append(temp)
            if request.method=="POST":
                exdata = Extractdata()
                batch = request.form.get('batch')
                department = request.form.get('department')
                d = exdata.get_scholars(batch,department)
                users = d[2]

            return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/promoting',methods=['POST','GET'])
def promoting():
    try:
        if session['logged_in']==True:
            u = UserEdits()
            ex = Extractdata()
            buser = ex.get_user("Research Scholar")
            print(buser.count())
            batch_object = Batch()
            batches = batch_object.get_batches()
            deplist = []
            departments = batch_object.get_departments()
            for i in departments:
                temp = {
                "depname":i,
                "djoin":i.replace(" ","")
                }
                deplist.append(temp)
            if request.method=="POST":
                email = request.form.get('email')
                batch = request.form.get('batch')
                department = request.form.get('department')
                d = ex.get_scholars(batch,department)
                users = d[2]
                if request.form['submitf']=="promote":
                    euser = ex.get_users_by_id(email,"Research Scholar")
                    esem = euser[0]['semesters'][0]
                    
                    if esem['sem1']=="0":
                        print("sem1")
                        esem['sem1'] = "1"
                        esem['next'] = "sem 2"
                        esem['prev'] = "sem 1"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    print("hello")
                    if esem['sem2']=="0":
                        print("sem2")
                        esem['sem2'] = "1"
                        esem['next'] = "sem 3"
                        esem['prev'] = "sem 2"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem3']=="0":
                        print("sem3")
                        esem['sem3'] = "1"
                        esem['next'] = "sem 4"
                        esem['prev'] = "sem 3"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem4']=="0":
                        print("sem4")
                        esem['sem4'] = "1"
                        esem['next'] = "sem 5"
                        esem['prev'] = "sem 4"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem5']=="0":
                        print("sem5")
                        esem['sem5'] = "1"
                        esem['next'] = "sem 6"
                        esem['prev'] = "sem 5"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem6']=="0":
                        print("sem6")
                        esem['sem6'] = "1"
                        esem['next'] = "none"
                        esem['prev'] = "sem 6"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                if request.form['submitf']=="demote":
                    euser = ex.get_users_by_id(email,"Research Scholar")
                    esem = euser[0]['semesters'][0]
                    
                    if esem['sem6']=="1":
                        print("sem6")
                        esem['sem6'] = "0"
                        esem['next'] = "sem 6"
                        esem['prev'] = "sem 5"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem5']=="1":
                        print("sem5")
                        esem['sem5'] = "0"
                        esem['next'] = "sem 5"
                        esem['prev'] = "sem 4"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem4']=="1":
                        print("sem4")
                        esem['sem4'] = "0"
                        esem['next'] = "sem 4"
                        esem['prev'] = "sem 3"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem3']=="1":
                        print("sem3")
                        esem['sem3'] = "0"
                        esem['next'] = "sem 3"
                        esem['prev'] = "sem 2"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem2']=="1":
                        print("sem2")
                        esem['sem2'] = "0"
                        esem['next'] = "sem 2"
                        esem['prev'] = "sem 1"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
                    if esem['sem1']=="1":
                        print("sem1")
                        esem['sem1'] = "0"
                        esem['next'] = "sem 1"
                        esem['prev'] = "none"
                        u.replace_sem(email,esem)
                        return render_template('admin/promote.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)

            return redirect(url_for('admin.promote'))
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
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
            f = request.files['file']
            filename = f.filename
            if user_type == "Research Supervisor":
                bpath = "supervisors"
            if user_type == "Research Co-Supervisor":
                bpath = "cosupervisors"
            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + "registrations/" + bpath)):
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + "registrations/" + bpath))
            path = os.path.join(app.config['UPLOAD_FOLDER']+"registrations/" + bpath,filename)
            main_path = path.split("static/")[1]
            main_path = main_path.split("\\")[0]
            main_path = main_path + "/" + filename
            print(main_path)
            f.save(path)

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
                "password":"mitdefault",
                "phone":request.form.get('phone'),
                "dob":request.form.get('dob'),
                "department":request.form.get('department'),
                "subdepartment":subdept,
                "address":request.form.get('address'),
                "gender":request.form.get('gender'),
                "nationality":request.form.get('nationality'),
                "twitter":request.form.get('twitter'),
                "skype":request.form.get('skype'),
                "facebook":request.form.get('facebook'),
                "github":request.form.get('repos'),
                "profile_pic":filename,
                "profile_pic_link":main_path,
                "status":"1",
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
    specialusers_object = Supervisors()
    try:
        if request.method == 'POST':
            user_type = "Special User"
            email = request.form.get('email')
            f = request.files['file']
            filename = f.filename
            bpath = "specialusers"
            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + "registrations/" + bpath)):
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + "registrations/" + bpath))
            path = os.path.join(app.config['UPLOAD_FOLDER']+"registrations/" + bpath,filename)
            main_path = path.split("static/")[1]
            main_path = main_path.split("\\")[0]
            main_path = main_path + "/" + filename
            print(main_path)
            f.save(path)
            
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
                "password":"mitdefault",
                "phone":request.form.get('phone'),
                "dob":request.form.get('dob'),
                "address":request.form.get('address'),
                "gender":request.form.get('gender'),
                "nationality":request.form.get('nationality'),
                "twitter":request.form.get('twitter'),
                "skype":request.form.get('skype'),
                "facebook":request.form.get('facebook'),
                "github":request.form.get('repos'),
                "info":request.form.get('info'),
                "profile_pic":filename,
                "profile_pic_link":main_path,
                "status":"1",
                "user_type":user_type
            }
            registration_status = specialusers_object.save_supervisor(user,user_type)
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
            exdata = Extractdata()
            user = []
            if request.method=="POST":
                email = request.form.get('email')
                usertype = request.form.get('usertype')
                user = exdata.get_users_by_id(email,usertype)
                if user.count()>0:
                    user = user[0]
                else:
                    user = []
            return render_template('admin/editusers.html', user = user)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/editing',methods=['POST','GET'])
def editing():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            batch_object = Batch()
            departments = list(batch_object.get_departments())
            supers = exdata.get_supervisors()
            cosupers = exdata.get_cosupervisors()
            ue = UserEdits()
            if request.method=="POST":
                if request.form['submitf']=="edit":
                    email = request.form.get('email')
                    usertype = request.form.get('usertype')
                    print(email)
                    print(usertype)
                    user = exdata.get_users_by_id(email,usertype)
                    user = user[0]

                if request.form['submitf']=="update_profile":
                    print("Hello Updater")
                    email = request.form.get('uemail')
                    usertype = request.form.get('uusertype')
                    batch = request.form.get('ubatch')
                    print(email)
                    print(usertype)
                    user = exdata.get_users_by_id(email,usertype)
                    user = user[0]
                    data = {}
                    scholar_details = ['first_name','last_name','phone','address','dob','gender','nationality','department','supervisor','cosupervisor','twitter','facebook','skype','github']
                    supervisor_details = ['first_name','last_name','phone','address','dob','gender','nationality','department','subdepartment','twitter','facebook','skype','github']
                    special_details = ['title','first_name','last_name','phone','address','dob','gender','nationality','twitter','facebook','skype','github','info']
                    if usertype == 'Research Scholar':
                        for i in scholar_details:
                            temp = request.form.get(i)
                            if temp != None and temp!="None" and temp!='':
                                data[i] = temp
                        print(data)
                    elif usertype == 'Research Supervisor' or usertype=='Research Co-Supervisor':
                        for i in supervisor_details:
                            temp = request.form.get(i)
                            if temp != None and temp!="None" and temp!='':
                                data[i] = temp
                        print(data)
                    elif usertype == 'Special User':
                        for i in special_details:
                            temp = request.form.get(i)
                            if temp != None and temp!="None" and temp!='':
                                data[i] = temp
                        print(data)
                    else:
                        pass
                    f = request.files['file']
                    print(f)
                    filename = f.filename
                    if filename =="":
                        pass
                    else:
                        if usertype == "Research Scholar":
                            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + batch + "/" + email)):
                                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + batch + "/" + email))
                            path = os.path.join(app.config['UPLOAD_FOLDER']+batch + "/" + email,filename)
                        else:
                            if usertype == "Research Supervisor":
                                bpath = "supervisors"
                            if usertype == "Research Co-Supervisor":
                                bpath = "cosupervisors"
                            if usertype == "Special User":
                                bpath = "specialusers"
                            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + "registrations/" + bpath)):
                                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + "registrations/" + bpath))
                            path = os.path.join(app.config['UPLOAD_FOLDER']+"registrations/" + bpath,filename)
                        main_path = path.split("static/")[1]
                        main_path = main_path.split("\\")[0]
                        main_path = main_path + "/" + filename
                        print(main_path)
                        f.save(path)
                        data['profile_pic'] = filename
                        data['profile_pic_link'] = main_path
                    stat = ue.update_prof(usertype,data,email)
                    if stat:
                        flash("Profile Updated Successfully. If the changes do not load, refresh once!")
            return render_template('admin/edit_profile.html',user=user,departments=departments,supers=supers,cosupers=cosupers)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/blockusers',methods=['POST','GET'])
def blockusers():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            busers = exdata.get_blocked_users()
            print(busers)
            if busers:
                pass
            else:
                busers = []
            user = []
            if request.method=="POST":
                email = request.form.get('email')
                usertype = request.form.get('usertype')
                user = exdata.get_users_by_id(email,usertype)
                if user.count()>0:
                    user = user[0]
                else:
                    user = []
            return render_template('admin/blockusers.html', user = user, busers = busers)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/blocking',methods=['POST','GET'])
def blocking():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            if request.method=="POST":
                if request.form['submitf']=="block":
                    email = request.form.get('email')
                    usertype = request.form.get('usertype')
                    print(email)
                    print(usertype)
                    ue = UserEdits()
                    stat = ue.block_user(email,usertype)
                    if stat:
                        flash("User Blocked Successfully")
                if request.form['submitf']=="unblock":
                    email = request.form.get('email')
                    usertype = request.form.get('usertype')
                    print(email)
                    print(usertype)
                    print("unblock")
                    ue = UserEdits()
                    stat = ue.unblock_user(email,usertype)
                    if stat:
                        flash("User Unblocked Successfully")
            return redirect(url_for('admin.blockusers'))
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/removeusers',methods=['POST','GET'])
def removeusers():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            user = []
            if request.method=="POST":
                email = request.form.get('email')
                usertype = request.form.get('usertype')
                user = exdata.get_users_by_id(email,usertype)
                if user.count()>0:
                    user = user[0]
                else:
                    user = []
            return render_template('admin/removeusers.html', user = user)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/removing',methods=['POST','GET'])
def removing():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            if request.method=="POST":
                if request.form['submitf']=="remove":
                    email = request.form.get('email')
                    usertype = request.form.get('usertype')
                    print(email)
                    print(usertype)
                    ue = UserEdits()
                    stat = ue.remove_user(email,usertype)
                    if stat:
                        flash("User Removed Successfully")
            return redirect(url_for('admin.removeusers'))
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_scholars',methods=['POST','GET'])
def view_scholars():
    try:
        if session['logged_in']==True:
            batch_object = Batch()
            exdata = Extractdata()
            batches = batch_object.get_batches()
            departments = batch_object.get_departments()
            deplist = []
            for i in departments:
                temp = {
                "depname":i,
                "djoin":i.replace(" ","")
                }
                deplist.append(temp)
            users = []
            return render_template('admin/view_scholars.html', batches=batches, departments=deplist, users=users)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/scholars_viewing',methods=['POST','GET'])
def scholars_viewing():
    try:
        if session['logged_in']==True:
            users = ""
            if request.method=="POST":
                batch_object = Batch()
                exdata = Extractdata()
                batch = request.form.get('batch')
                department = request.form.get('department')
                d = exdata.get_scholars(batch,department)
                batch = d[0]
                department = d[1]
                users = d[2]
                batches = batch_object.get_batches()
                departments = batch_object.get_departments()
                deplist = []
            for i in departments:
                temp = {
                "depname":i,
                "djoin":i.replace(" ","")
                }
                deplist.append(temp)

            return render_template('admin/view_scholars.html',users=users,batches=batches, departments=deplist, batch=batch, department=department)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_supervisors',methods=['POST','GET'])
def view_supervisors():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            users = exdata.get_user("Research Supervisor")
            return render_template('admin/view_supervisors.html',users=users)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_cosupervisors',methods=['POST','GET'])
def view_cosupervisors():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            users = exdata.get_user("Research Co-Supervisor")
            return render_template('admin/view_cosupervisors.html',users=users)
        else:
            return redirect(url_for("admin.login"))
    except Exception as error:
        print(error)
        return render_template('admin/admin_login.html')

@admin.route('/view_authorities',methods=['POST','GET'])
def view_authorities():
    try:
        if session['logged_in']==True:
            exdata = Extractdata()
            users = exdata.get_user("Special User")
            return render_template('admin/view_authorities.html', users=users)
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