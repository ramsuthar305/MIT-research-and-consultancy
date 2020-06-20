import hashlib
from app import *
from flask import session
import os 
#from pyresparser import ResumeParser
from bson import ObjectId



class Forum_model:
	def __init__(self):
		self.mongo = mongo.db 
	
	def new_post(self,data):
		try:
			post = self.mongo.forum.insert_one(data)
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error
		
	def new_answer(self,answer,post_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id)},{"$push":{"answers":answer}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_report(self,report,post_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id)},{"$push":{"reports":report}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_upvote(self,upvote_data,post_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id)},{"$push":{"upvotes":upvote_data}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_downvote(self,downvote_data,post_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id)},{"$push":{"downvotes":downvote_data}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_comment(self,comment_data,post_id,answer_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id),"answers":{"$elemMatch":{"_id":ObjectId(answer_id)}}},{"$push":{"answer.$.comments":comment_data}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_report(self,report_data,post_id,answer_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id),"answers":{"$elemMatch":{"_id":ObjectId(answer_id)}}},{"$push":{"answer.$.reports":report_data}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_answer_like(self,answer_like_data,post_id,answer_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id),"answers":{"$elemMatch":{"_id":ObjectId(answer_id)}}},{"$push":{"answer.$.answer_likes":answer_like_data}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error

	def new_answer_dislike(self,answer_dislike_data,post_id,answer_id):
		try:
			status = self.mongo.forum.update_one({"_id":ObjectId(post_id),"answers":{"$elemMatch":{"_id":ObjectId(answer_id)}}},{"$push":{"answer.$.answer_dislikes":answer_dislike_data}})
			post = self.mongo.forum.find_one({"_id":ObjectId(post_id)})
			if post != None:
				return post
			else:
				return False
		except Exception as error:
			print('In exception :',error)
			return error