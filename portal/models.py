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
						  {"password": password},{"status":"0"}]})
			print(login_result)
			if login_result is not None:
				if login_result["user_type"]=="Research Scholar":
					user_info=self.mongo.researcher.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["first_name"]+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
					return True
				elif login_result["user_type"]=="Research Supervisor":
					user_info=self.mongo.supervisor.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["first_name"]+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
					return True
				elif login_result["user_type"]=="Research Co-Supervisor":
					user_info=self.mongo.cosupervisor.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["first_name"]+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
					return True
				elif login_result["user_type"]=="Special User":
					user_info=self.mongo.specialuser.find_one({"_id":login_result["uid"]})
					session["email"] = user_info["email"]
					session["name"] = user_info["title"]+user_info["first_name"]+user_info["last_name"]
					session["logged_in"] = True
					session["user_type"] = user_info['user_type']
					session['id'] = str(user_info["_id"])
					session['department'] = str(user_info["department"])
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


	def get_resource(self):
		try:
			result=mongo.db.resource.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "Something went wrong"


	def search(self,search_text):
		try:
			result=mongo.db.resource.find({"$text": {"$search": search_text}})

			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "Something went wrong"


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

