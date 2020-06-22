from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
import hashlib
import json
from datetime import datetime, date
#custom imports
from app import *
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


@portal.route('/publication')
def publication():
    
    return render_template('portal/publication.html')

    


@portal.route('/profile')
def profile():
    exdata = Extract_Data()
    user = exdata.get_researcher()
    sub = Submissions()
    st = Student_Resources()
    quests=sub.get_all_questions()
    answers=sub.get_questions_answered_by_user()
    qidlist=[]
    for i in answers:
    	qidlist.append(i['qid'])
    resource = st.fetch_resource()
    resource1 = st.fetch_resource()
    resource2 = st.fetch_resource()
    return render_template('portal/userprofile.html',user=user,quests=quests,answers=answers,qidlist=qidlist,resource=resource,resource1=resource1,resource2=resource2)

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
        session.clear()
        return redirect(url_for('portal.signin'))
    except Exception as error:
        print(error)
        return redirect(url_for('portal.signin'))


@portal.route('/supervisors_panel', methods=['POST','GET'])
def supervisors_panel():
    exdata = Extract_Data()
    batches=exdata.get_batches()
    sub = Submissions()
    st = Student_Resources()
    quests = sub.get_questions_by_author(session['id'])
    restbatches = []
    for i in range(0,batches.count()):
        restbatches.append(batches[i])
    restsub = []
    for i in range(0,quests.count()):
        restsub.append(quests[i])
    qanswered = sub.get_questions_answered()
    qidlist=[]
    for i in qanswered:
    	qidlist.append(i['qid'])
    print(qidlist)

    verify_resource = st.fetch_resources_by_guide()
    verified_resource = st.fetch_resources_by_guide()

    try:
        if session['logged_in']==True:
            return render_template('portal/supervisors_panel.html',restbatches=restbatches,quests=quests,batches=batches, restsub=restsub,qidlist=qidlist,verify_resource=verify_resource,verified_resource=verified_resource)
        else:
            return redirect(url_for("portal.index"))
    except Exception as error:
        print(error)
        return render_template('portal/index.html')


@portal.route('/submission_request', methods=['POST','GET'])
def submission_request():
    exdata = Extract_Data()
    batches=exdata.get_batches()
    sub = Submissions()
    try:
        if request.method == 'POST':
            
            f = request.files['file']
            filename = f.filename
            path = os.path.join(app.config['UPLOAD_FOLDER']+"submissions",filename)
            main_path = path.split("static/")[1]
            main_path = main_path.split("\\")[0]
            main_path = main_path + "/" + filename
            print(main_path)
            f.save(path)
            temp = request.form.get('title')
            temp = temp.replace(" ","")

            qid = temp+session["id"]+request.form.get('batch')
            data = {
            "qid":qid,
            "title":request.form.get('title'),
            "tjoin":temp,
            "department":request.form.get('department'),
            "batch":request.form.get('batch'),
            "date_uploaded":str(date.today()),
            "deadline":request.form.get('deadline'),
            "description":request.form.get('description'),
            "pdf":main_path,
            "pdfname":filename,
            "author":session["id"],
            "answers":"0",
            "solution":[]
            }
            print(data)
            status = sub.add_submission(data)
            #sub.upload_file(file_data,f,"pdf",request.form.get('title'))
            flash("Assignment Posted Successfully")
            return redirect(url_for('portal.supervisors_panel'))
        else:
            return redirect(url_for('portal.supervisors_panel'))
    except Exception as error:
        print(error)
        return redirect(url_for('portal.signin'))

@portal.route('/submission_answers', methods=['POST','GET'])
def submission_answers():
	sub = Submissions()
	if request.method == 'POST':
		f = request.files['file']
		filename = f.filename
		if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + "submissions")):
			os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + "submissions"))
		path = os.path.join(app.config['UPLOAD_FOLDER']+"submissions",filename)
		main_path = path.split("static/")[1]
		main_path = main_path.split("\\")[0]
		main_path = main_path + "/" + filename
		print(main_path)
		f.save(path)
		check = request.form.get('linker')
		print(check)
		q = sub.get_question_by_id(check)
		sol = q['solution']
		answer = {
		"name":session["name"],
		"email":session["email"],
		"batch":session["batch"],
		"department":session["department"],
		"question_id":check,
		"pdf_link":main_path,
		"pdf_name":filename,
		"grades":"None",
		"status":"0"
		}
		up = q['answers']
		up = str(int(up)+1)
		sol.append(answer)
		print(sol)
		status = sub.update_subs(check,sol,up)
		flash("Assignment Submitted Successfully")
		return redirect(url_for('portal.profile'))
	return redirect(url_for('portal.profile'))

@portal.route('/evalsubmission', methods=['POST','GET'])
def evalsubmission():
	sub = Submissions()
	quests = sub.get_questions_by_author(session['id'])
	store = []
	change = {}
	grades=""
	if request.method=="POST":
		email = request.form.get('email')
		qid = request.form.get('qid')
		grades = request.form.get('grades')
		print(grades)
		if grades:
			pass
		else:
			grades = "None"
		for i in quests:
			if i['qid']==qid:
				store = i['solution']
				break
		print(store)

		if request.form['submit_button']=="accept":
			for i in store:
				if i['email']==email:
					i['status']='1'
					i['grades']=grades
					break
			print(store)
			result = sub.update_eval(qid,store)

		if request.form['submit_button']=="reject":
			for i in store:
				if i['email']==email:
					i['status']='2'
					break
			print(store)
			result = sub.update_eval(qid,store)

		if request.form['submit_button']=="delete":
			result = sub.delete_question(qid)
			flash("Assignment Deleted Successfully")
	return redirect(url_for('portal.supervisors_panel'))


@portal.route('/student_resource', methods=['POST','GET'])
def student_resource():
	st = Student_Resources()
	if request.method=="POST":
		f = request.files['file']
		filename = f.filename
		if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + "studentresources")):
	 		os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + "studentresources"))
		path = os.path.join(app.config['UPLOAD_FOLDER']+"studentresources",filename)
		main_path = path.split("static/")[1]
		main_path = main_path.split("\\")[0]
		main_path = main_path + "/" + filename
		print(main_path)
		f.save(path)
		rid = request.form.get('title')+session['name']+filename
		data ={
		"title":request.form.get('title'),
		"rid":rid,
		"description":request.form.get('description'),
		"author":session['name'],
		"email":session['id'],
		"supervisor":request.form.get('supervisor'),
		"pdf_name":filename,
		"pdf_link":main_path,
		"uploaded_on":str(datetime.now()).split('.')[0],
		"status":"0",
		}
		result=st.add_student_resource(data)
		flash("Data Successfully Sent for Verification")
	return redirect(url_for('portal.profile'))

@portal.route('/evalresource', methods=['POST','GET'])
def evalresource():
	st = Student_Resources()
	if request.method=="POST":
		rid = request.form.get('rid')
		if request.form['submitbtn']=="verify":
			print("accept")
			print(rid)
			data = st.update_resource_by_id(rid,"1")
		if request.form['submitbtn']=="reject":
			print("reject")
			data = st.update_resource_by_id(rid,"2")

	return redirect(url_for('portal.supervisors_panel'))
