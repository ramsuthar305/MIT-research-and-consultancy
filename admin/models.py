import hashlib
from app import *
from flask import session
from bson import ObjectId

class Users:
	def __init__(self):
		self.mongo = mongo.db

	def reset_admin(self):
		try:
			result = mongo.db.admin.drop()
			password = "admin"
			h = hashlib.md5(password.encode())
			encpass = h.hexdigest()
			print(encpass)
			user = {
			"_id":"mitrcadmin@gmail.com",
			"first_name":"MIT",
			"last_name":"Admin",
			"email":"mitrcadmin@gmail.com",
			"password":encpass,
			}
			result = mongo.db.admin.insert_one(user)
			print(result)
		except Exception as error:
			print(error)

	def admin_login(self,email,password):
		try:
			h = hashlib.md5(password.encode())
			encpass = h.hexdigest()
			result = mongo.db.admin.find({"$and":[{"email":email},{"password":encpass}]})
			if result.count()>0:
				result = result[0]
				session['logged_in'] = True
				session['id'] = result['email']
				session['name'] = result['first_name'] + " " + result['last_name']
				session['email'] = result['email']
				session['user_type'] = "admin"
				return True
			else:
				return False
		except Exception as error:
			print(error)

	def check_old_pass(self,val):
		try:
			h = hashlib.md5(val.encode())
			val = h.hexdigest()
			result = mongo.db.admin.find({"$and":[{"email":session['email']},{"password":val}]})
			if result.count()>0:
				return True
			else:
				return False
		except Exception as error:
			print(error)

	def update_pass(self,val):
		try:
			h = hashlib.md5(val.encode())
			val = h.hexdigest()
			result = mongo.db.admin.update({"email":session['email']},{"$set":{"password":val}})
		except Exception as error:
			print(error)

class Supervisors:
	def __init__(self):
		self.mongo = mongo.db

	def save_supervisor(self,user,user_type):
		try:
			if user_type=="Research Supervisor":
				result = mongo.db.supervisor.insert_one(user)
			elif user_type=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.insert_one(user)
			elif user_type=="Special User":
				result = mongo.db.specialuser.insert_one(user)
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
				return True

			else:
				print("\nSomething went wrong: ",result)
				return False
		except Exception as error:
			print(error)
			if error.code == 11000:
				return "User already exists"

class SpecialUsers:
	def __init__(self):
		self.mongo = mongo.db

	def save_specialuser(self,user,user_type):
		try:
			if user_type=="Special User":
				result = mongo.db.specialuser.insert_one(user)
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
				return True

			else:
				print("\nSomething went wrong: ",result)
				return False
		except Exception as error:
			print(error)
			if error.code == 11000:
				return "User already exists"

class Batch:
	def __init__(self):
		self.mongo =mongo.db

	def add_batch(self,data):
		try:
			result=mongo.db.batch.insert_one(data)
			if result:
				return result.inserted_id
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

	def activate_batch(self,data):
		try:
			fetcher=mongo.db.batch.find()
			for i in fetcher:
				result=mongo.db.batch.update_one({"_id":i['_id']},{"$set":{"status":"0"}})
			result1=mongo.db.batch.update_one({"batch_name":data},{"$set":{"status":"1"}})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def expire_batch(self,data):
		try:
			result1=mongo.db.batch.update_one({"batch_name":data},{"$set":{"expire":"1"}})
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

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

	def fetch_pending(self):
		try:
			result = mongo.db.tempuser.find()
			return result
		except Exception as error:
			print(error)

	def authorization(self,userid,op):
		try:
			if op=="1":
				result = mongo.db.tempuser.find({"_id":userid})
				user = result[0]
				main = mongo.db.researcher.insert_one(user)
				active = mongo.db.researcher.update_one({'_id':userid},{"$set":{"status":"1"}})
				result=mongo.db.authentication.insert_one({
					"uid":user["_id"],
					"email":user["email"],
					"password":user["password"],
					"user_type":user["user_type"],
					"status":user["status"]
				})
				active = mongo.db.authentication.update_one({'uid':userid},{"$set":{"status":"1"}})
				rem = mongo.db.tempuser.remove({"_id":userid})
			if op=="2":
				result = mongo.db.tempuser.remove({"_id":userid})
			return result
		except Exception as error:
			print(error)

	def get_departments(self):
		try:
			departments = self.mongo.departments.find_one()
			return departments['departments']
		except Exception as error:
			print('In exception :', error)
			return []

class Extractdata:
	def __init__(self):
		self.mongo =mongo.db

	def get_user(self,usertype):
		try:
			if usertype == "Research Scholar":
				result=mongo.db.researcher.find()
			if usertype == "Research Supervisor":
				result=mongo.db.supervisor.find()
			if usertype == "Research Co-Supervisor":
				result=mongo.db.cosupervisor.find()
			if usertype == "Special User":
				result=mongo.db.specialuser.find()
			if result:
				return result
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	def get_scholars(self,batch,department):
		try:
			result=mongo.db.researcher.find({"$and":[{"batch":batch},{"department":department}]})
			return (list([batch,department,result]))
		except Exception as error:
			return False

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

	def get_blocked_users(self):
		try:
			L = []
			result1 = mongo.db.researcher.find({"status":"2"})
			result2 = mongo.db.supervisor.find({"status":"2"})
			result3 = mongo.db.cosupervisor.find({"status":"2"})
			result4 = mongo.db.specialuser.find({"status":"2"})
			if result1.count()>0:
				L.append(result1)
			if result2.count()>0:
				L.append(result2)
			if result3.count()>0:
				L.append(result3)
			if result4.count()>0:
				L.append(result4)
			return L

		except Exception as error:
			print(error)

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

class UserEdits:
	def block_user(self,email,usertype):
		try:
			if usertype=="Research Scholar":
				result = mongo.db.researcher.update({"email":email},{"$set":{"status":"2"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"2"}})
				return result
			if usertype=="Research Supervisor":
				result = mongo.db.supervisor.update({"email":email},{"$set":{"status":"2"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"2"}})
				return result
			if usertype=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.update({"email":email},{"$set":{"status":"2"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"2"}})
				return result
			if usertype=="Special User":
				result = mongo.db.specialuser.update({"email":email},{"$set":{"status":"2"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"2"}})
				return result
		except Exception as error:
			print(error)

	def unblock_user(self,email,usertype):
		try:
			if usertype=="Research Scholar":
				result = mongo.db.researcher.update({"email":email},{"$set":{"status":"1"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"1"}})
				return result
			if usertype=="Research Supervisor":
				result = mongo.db.supervisor.update({"email":email},{"$set":{"status":"1"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"1"}})
				return result
			if usertype=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.update({"email":email},{"$set":{"status":"1"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"1"}})
				return result
			if usertype=="Special User":
				result = mongo.db.specialuser.update({"email":email},{"$set":{"status":"1"}})
				result = mongo.db.authentication.update({"uid":email},{"$set":{"status":"1"}})
				return result
		except Exception as error:
			print(error)

	def remove_user(self,email,usertype):
		try:
			if usertype=="Research Scholar":
				result = mongo.db.researcher.remove({"email":email})
				result = mongo.db.authentication.remove({"uid":email})
				return result
			if usertype=="Research Supervisor":
				result = mongo.db.supervisor.remove({"email":email})
				result = mongo.db.authentication.remove({"uid":email})
				return result
			if usertype=="Research Co-Supervisor":
				result = mongo.db.cosupervisor.remove({"email":email})
				result = mongo.db.authentication.remove({"uid":email})
				return result
			if usertype=="Special User":
				result = mongo.db.specialuser.remove({"email":email})
				result = mongo.db.authentication.remove({"uid":email})
				return result
		except Exception as error:
			print(error)

	def replace_sem(self,email,sem):
		try:
			L = []
			L.append(sem)
			result = mongo.db.researcher.update({"email":email},{"$set":{"semesters":L}})
			return result
		except Exception as error:
			print(error)

	def timepass(self):
		try:
			L = []
			sem = {
			"sem1":"0",
			"sem2":"0",
			"sem3":"0",
			"sem4":"0",
			"sem5":"0",
			"sem6":"0",
			}
			L.append(sem)
			result = mongo.db.researcher.update({"email":"safirmotiwala@gmail.com"},{"$set":{"semesters":L}})
			result = mongo.db.researcher.update({"email":"ramsuthar305@gmail.com"},{"$set":{"semesters":L}})
			result = mongo.db.researcher.update({"email":"vinayak@gmail.com"},{"$set":{"semesters":L}})
		except Exception as e:
			raise e

<<<<<<< HEAD
	def get_profiles(self,job_id):
		profiles=mongo.db.shortlist.find({"job_id":job_id})
		users=Users()
		all_profiles=[]
		for profile in profiles:
			user=users.get_user_by_id(profile['user_id'])
			user['score']=profile['aptiscore']+profile['personalityscore']+profile['skillscore']
			user['outoff']=profile['totalScore']
			all_profiles.append(user)
		print(all_profiles)
		return all_profiles



class Resource:
	def __init__(self):
		self.mongo =mongo.db

	def add_resource(self,data):
		try:
			result=mongo.db.resource.insert_one(data)
			if result:
				return results
			else:
				return False
		except Exception as error:
			print(error)
			return "something went wrong"

	
=======
	def update_prof(self,usertype,data,email):
		try:
			if usertype == "Research Scholar":
				for i,j in zip(data,data.values()):
					result = mongo.db.researcher.update({"_id":email},{"$set":{i:j}})
			if usertype == "Research Supervisor":
				for i,j in zip(data,data.values()):
					result = mongo.db.supervisor.update({"_id":email},{"$set":{i:j}})
			if usertype == "Research Co-Supervisor":
				for i,j in zip(data,data.values()):
					result = mongo.db.cosupervisor.update({"_id":email},{"$set":{i:j}})
			if usertype == "Special User":
				for i,j in zip(data,data.values()):
					result = mongo.db.specialuser.update({"_id":email},{"$set":{i:j}})
			return True
		except Exception as error:
			print(error)
>>>>>>> 9b688b2c7915e1d26963d62d2522f585170fa73d
