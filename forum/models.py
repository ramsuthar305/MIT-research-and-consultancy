import hashlib
from app import *
from flask import session
import os
# from pyresparser import ResumeParser
from bson import ObjectId


class Forum_model:
    def __init__(self):
        self.mongo = mongo.db

    def get_all_posts(self):
        try:
            posts = list(self.mongo.forum.find({"category":session['department']}))
            print(posts)
            if posts != None:
                return posts
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return []

    def new_post(self, data):
        try:
            post = self.mongo.forum.insert_one(data)
            post = self.mongo.forum.find_one(
                {"_id": ObjectId(post.inserted_id)})
            print(post)
            if post != None:
                post['created_on']=str(post['created_on'])
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return False

    def new_answer(self, answer, post_id):
        try:
            status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                "$push": {"answers": answer}})
            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_report(self, report, post_id):
        try:
            status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                "$push": {"reports": report}})
            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_upvote(self, upvote_data, post_id):
        try:
            upvote_exists = list(self.mongo.forum.find(
                {"upvotes": {"$elemMatch": {"uid": upvote_data['uid']}}}))
            if len(upvote_exists) == 0:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                    "$push": {"upvotes": upvote_data}})
            else:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                    "$pull": {"upvotes": {"uid": upvote_data['uid']}}})
            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_downvote(self, downvote_data, post_id):
        try:
            downvote_exists = list(self.mongo.forum.find(
                {"downvotes": {"$elemMatch": {"uid": downvote_data['uid']}}}))
            if len(downvote_exists) == 0:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                    "$push": {"downvotes": downvote_data}})
            else:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                    "$pull": {"downvotes": {"uid": downvote_data['uid']}}})
            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_comment(self, comment_data, post_id, answer_id):
        try:
            status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                "_id": ObjectId(answer_id)}}}, {"$push": {"answers.$.comments": comment_data}})
            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_answer_report(self, report_data, post_id, answer_id):
        try:
            status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                "_id": ObjectId(answer_id)}}}, {"$push": {"answers.$.reports": report_data}})
            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_answer_upvote(self, answer_upvote_data, post_id, answer_id):
        try:
            downvote_exists = list(self.mongo.forum.find(
                {"answers.downvotes": {"$elemMatch": {"uid": answer_upvote_data['uid']}}}))
            print("\n\n this is sttus: ", downvote_exists)
            if len(downvote_exists) != 0:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                                                     "_id": ObjectId(answer_id)}}}, {"$pull": {"answers.$.downvotes":  {"uid": answer_upvote_data['uid']}}})

            upvote_exists = list(self.mongo.forum.find(
                {"answers.upvotes": {"$elemMatch": {"uid": answer_upvote_data['uid']}}}))
            print("\n\n this is sttus: ", upvote_exists)
            if len(upvote_exists) == 0:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                                                     "_id": ObjectId(answer_id)}}}, {"$push": {"answers.$.upvotes": answer_upvote_data}})
            else:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                                                     "_id": ObjectId(answer_id)}}}, {"$pull": {"answers.$.upvotes":  {"uid": answer_upvote_data['uid']}}})

            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def new_answer_downvote(self, answer_downvote_data, post_id, answer_id):
        try:
            upvote_exists = list(self.mongo.forum.find(
                {"answers.upvotes": {"$elemMatch": {"uid": answer_downvote_data['uid']}}}))
            print("\n\n this is sttus: ", upvote_exists)
            if len(upvote_exists) != 0:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                                                     "_id": ObjectId(answer_id)}}}, {"$pull": {"answers.$.upvotes":  {"uid": answer_downvote_data['uid']}}})
            downvote_exists = list(self.mongo.forum.find(
                {"answers.downvotes": {"$elemMatch": {"uid": answer_downvote_data['uid']}}}))
            print("\n\n this is sttus: ", downvote_exists)
            if len(downvote_exists) == 0:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                                                     "_id": ObjectId(answer_id)}}}, {"$push": {"answers.$.downvotes": answer_downvote_data}})
            else:
                status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {"_id": ObjectId(
                    answer_id)}}}, {"$pull": {"answers.$.downvotes":  {"uid": answer_downvote_data['uid']}}})

            post = self.mongo.forum.find_one({"_id": ObjectId(post_id)})
            if post != None:
                return post
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def delete_post(self, post_id):
        try:
            status = self.mongo.forum.remove({"_id": ObjectId(post_id)})
            print("\nthis is delete status: ", status['n'])
            if status['n'] != 0:
                return True
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def delete_answer(self, post_id, answer_id):
        try:
            status = self.mongo.forum.update_one({"_id": ObjectId(post_id)}, {
                                                 "$pull": {"answers": {"_id": ObjectId(answer_id)}}})
            print("\nthis is delete status: ", status.modified_count)
            if status.modified_count != 0:
                return True
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error

    def delete_comment(self, post_id, answer_id, comment_id):
        try:
            status = status = self.mongo.forum.update_one({"_id": ObjectId(post_id), "answers": {"$elemMatch": {
                                                          "_id": ObjectId(answer_id)}}}, {"$pull": {"answers.$.comments":  {"_id": ObjectId(comment_id)}}})
            print("\nthis is delete status: ", status.modified_count)
            if status.modified_count != 0:
                return True
            else:
                return False
        except Exception as error:
            print('In exception :', error)
            return error
