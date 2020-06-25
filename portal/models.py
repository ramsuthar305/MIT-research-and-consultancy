import hashlib
from app import *
from flask import session
import os 
#from pyresparser import ResumeParser
from bson import ObjectId


class Users:
	def __init__(self):
		self.mongo = mongo.db

	def check_user_exists(self, username):
		result = self.mongo.users.find_one({"$or": [{"username": username}, {"phone": username}]})
		if result:
			return True
		else:
			return False

	def temp_user(self,user):
		try:
			result=mongo.db.tempuser.insert_one(user)
			return result
		except Exception as error:
			print(error)

	def save_user(self,user,user_type):
		try:
			if user_type=="Research Scholar":
				result = mongo.db.researcher.insert_one(user)
			else:
				result = mongo.db.USERTYPE.insert_one(user)
			if result:
				result=mongo.db.authentication.insert_one({
					"uid":user["_id"],
					"email":user["email"],
					"password":user["password"],
					"user_type":user["user_type"],
					"status":user["status"]
				})
				if result:
					print(result)
					session["email"] = user["email"]
					session["name"] = user["first_name"]+" "+user["last_name"]
					session["logged_in"] = True
					session["user_type"] = user["user_type"]
					session['id'] = str(user["email"])
					session['department'] = str(user["department"])
					session['batch'] = str(user["batch"])
					return True
				else:
					print("\nSomething went wrong: ",result)
					return False
			else:
				print("\nSomething went wrong: ",result)
				return False
		except Exception as error:
			print(error)
			if error.code == 11000:
				return "User already exists"


	def login_user(self, username, password):
		try:
			login_result = self.mongo.authentication.find_one(
				{"$and": [{"$or": [{"uid": username}, {"email": username}]},
						  {"password": password},{"status":"1"}]})
			print(login_result)
			if login_result is not None:
				if login_result["user_type"]=="Research Scholar":
					user_info=self.mongo.researcher.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["first_name"]+" "+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
					session['batch'] = str(user_info["batch"])
					return True
				elif login_result["user_type"]=="Research Supervisor":
					user_info=self.mongo.supervisor.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["first_name"]+" "+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
					return True
				elif login_result["user_type"]=="Research Co-Supervisor":
					user_info=self.mongo.cosupervisor.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["first_name"]+" "+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
					return True
				elif login_result["user_type"]=="Special User":
					user_info=self.mongo.specialuser.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["title"]+" "+user_info["first_name"]+" "+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					return True
			else:
				return "User does not exist"
		except Exception as error:
			return error

	def get_user_profile(self):
		try:
			user_profile=self.mongo.users.find_one({"username": session["username"]})
			return (user_profile)
		except Exception as error:
			print(error)

	def check_old_pass(self,val):
		try:
			if session['user_type']=="Research Scholar":
				result = mongo.db.researcher.find({"$and":[{"email":session['email']},{"password":val}]})
			if session['user_type']=="Research Supervisor":
				result = mongo.db.supervisor.find({"$and":[{"email":session['email']},{"password":val}]})
			if session['user_type']=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.find({"$and":[{"email":session['email']},{"password":val}]})
			if session['user_type']=="Special User":
				result = mongo.db.specialuser.find({"$and":[{"email":session['email']},{"password":val}]})
			if result.count()>0:
				return True
			else:
				return False
		except Exception as error:
			print(error)

	def update_pass(self,val):
		try:
			if session['user_type']=="Research Scholar":
				result = mongo.db.researcher.update({"email":session['email']},{"$set":{"password":val}})
			if session['user_type']=="Research Supervisor":
				result = mongo.db.supervisor.update({"email":session['email']},{"$set":{"password":val}})
			if session['user_type']=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.update({"email":session['email']},{"$set":{"password":val}})
			if session['user_type']=="Special User":
				result = mongo.db.specialuser.update({"email":session['email']},{"$set":{"password":val}})
			result = mongo.db.authentication.update({"uid":session['email']},{"$set":{"password":val}})
		except Exception as error:
			print(error)

	# def upload_file(self, file_data, file, file_type):
	# 	try:
	# 		print('called')
	# 		if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"])):
	# 			os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"]))
	# 		file_path = os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"])
	# 		file.save(file_path + file_data["filename"])
	# 		file_result = os.path.exists(file_path + file_data["filename"])
	# 		print(file_result)
			
	# 		if file_result:
	# 			file_data["file_path"] = file_path.split("static/")[1]
				
	# 			if file_type=="pic":
	# 				if os.path.exists(file_data["file_path"]):
	# 					os.remove(file_data["file_path"])
	# 				result = self.mongo.users.update_one({"_id": session["id"]}, {"$set": {"profile_picture":file_data["file_path"] + file_data["filename"]}})
			
	# 			if file_type=="resume":
	# 				if os.path.exists(file_data["file_path"]):
	# 					os.remove(file_data["file_path"])
	# 				print(file_data['file_path'])
	# 				data = ResumeParser(os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"]+file_data["filename"])).get_extracted_data()
	# 				result = self.mongo.users.update_one({"_id": session["id"]}, {"$set": {"resume":file_data["file_path"] + file_data["filename"],"skills":data["skills"]}})
	# 		return True
	# 	except Exception as error:
	# 		print(error)
	# 		return True

class Extract_Data:
	def __init__(self):
		self.mongo =mongo.db

	def get_active_batch(self):
		try:
			result=mongo.db.batch.find({"status":"1"})
			result=result[0]['batch_name']
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_batches(self):
		try:
			result=mongo.db.batch.find({"expire":"0"})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_researcher(self):
		try:
			
			if session["user_type"]=="Research Scholar":
				result=mongo.db.researcher.find({"_id":session["id"]})
			elif session["user_type"]=="Research Supervisor":
				result=mongo.db.supervisor.find({"_id":session["id"]})
			elif session["user_type"]=="Research Co-Supervisor":
				result=mongo.db.cosupervisor.find({"_id":session["id"]})
			elif session["user_type"]=="Special User":
				result=mongo.db.specialuser.find({"_id":session["id"]})

			result=result[0]

			
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_supervisors(self):
		try:
			result=mongo.db.supervisor.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_cosupervisors(self):
		try:
			result=mongo.db.cosupervisor.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_specialuser(self):
		try:
			result=mongo.db.specialuser.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_users_by_id(self,email,usertype):
		try:
			if usertype=="Research Scholar":
				result = mongo.db.researcher.find({"email":email})
				return result
			if usertype=="Research Supervisor":
				result = mongo.db.supervisor.find({"email":email})
				return result
			if usertype=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.find({"email":email})
				return result
			if usertype=="Special User":
				result = mongo.db.specialuser.find({"email":email})
				return result

		except Exception as error:
			print(error)


class Submissions:
	def __init__(self):
		self.mongo =mongo.db

	def add_submission(self,data):
		try:
			result=mongo.db.submissions.insert_one(data)
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_questions_by_author(self,data):
		try:
			result=mongo.db.submissions.find({"author":data})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_all_questions(self):
		try:
			result=mongo.db.submissions.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_question_by_id(self,check):
		try:
			result=mongo.db.submissions.find({"qid":check})
			result=result[0]
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_questions_answered_by_user(self):
		try:
			result=mongo.db.submissions.find({"solution.email":session['email']})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_questions_answered(self):
		try:
			result=mongo.db.submissions.find({"answers":{"$gt":"0"}})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"


	def update_subs(self,check,sol,up):
		try:
			result=mongo.db.submissions.update_one({"qid":check},{"$set":{"solution":sol}})
			result1=mongo.db.submissions.update_one({"qid":check},{"$set":{"answers":up}})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def update_eval(self,check,sol):
		try:
			result=mongo.db.submissions.update_one({"qid":check},{"$set":{"solution":sol}})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def delete_question(self,check):
		try:
			result=mongo.db.submissions.remove({"qid":check})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def upload_file(self, file_data, file, file_type,title):
		try:
 			print('called')
	 		if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"])):
	 			os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"]))
	 		file_path = os.path.join(app.config['UPLOAD_FOLDER'] + file_data["directory"])
	 		#file.save(file_path + file_data["filename"])
	 		file.save(file_data["filename"])
	 		file_result = os.path.exists(file_path + file_data["filename"])
	 		print(file_result)
			
	 		if file_result:
	 			file_data["file_path"] = file_path.split("static/")[1]
				
	 			if file_type=="pic":
	 				if os.path.exists(file_data["file_path"]):
	 					os.remove(file_data["file_path"])
	 				result = self.mongo.submissions.update_one({"$and":[{"title": title},{"author":session['id']}]}, {"$set": {{"pdf":file_data["file_path"] + file_data["filename"]},{"pdfname":file_data["filename"]}}})
			
	 			if file_type=="pdf":
	 				if os.path.exists(file_data["file_path"]):
	 					os.remove(file_data["file_path"])
	 				print(file_data['file_path'])
	 				
	 				result = self.mongo.submissions.update_one({"$and":[{"title": title},{"author":session['id']}]}, {"$set": {{"pdf":file_data["file_path"] + file_data["filename"]}}})
	 		return True
		except Exception as error:
	 		print(error)
	 		return True

class Student_Resources:
	def __init__(self):
		self.mongo =mongo.db

	def add_student_resource(self,data):
		try:
			result=mongo.db.studentresource.insert_one(data)
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def fetch_resources_by_guide(self):
		try:
			result=mongo.db.studentresource.find({"supervisor":session['name']})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def fetch_resource(self):
		try:
			result=mongo.db.studentresource.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def update_resource_by_id(self,rid,temp):
		try:
			result=mongo.db.studentresource.update_one({"rid":rid},{"$set":{"status":temp}})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

class Collaborations:
	def __init__(self):
		self.mongo =mongo.db

	def add_col(self,data):
		try:
			result = mongo.db.collaborations.insert_one(data)
			return result
		except Exception as error:
			return "Something went wrong"

	def fetch_col_supervisor(self):
		try:
			result = mongo.db.collaborations.find({"supervisor_email":session['email']})
			if result:
				return result
			else:
				return False
		except Exception as error:
			return "Something went wrong"

	def fetch_col_researcher(self):
		try:
			result = mongo.db.collaborations.find({"student_email":session['email']})
			if result:
				return result
			else:
				return False
		except Exception as error:
			return "Something went wrong"

	def delete_col(self,cid):
		try:
			result = mongo.db.collaborations.remove({'cid':cid})
			return result
		except Exception as error:
			return "Something went wrong"

class Eresources:
	def __init__(self):
		self.mongo =mongo.db
	
	def get_data(self):
		try:
			result=list(mongo.db.resource.find())
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"