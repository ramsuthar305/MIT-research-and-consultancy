from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
import hashlib
import json
from datetime import datetime
#custom imports
from .models import Forum_model

forum_obj = Forum_model()

forum = Blueprint("forum", __name__, template_folder='../template', static_folder='../static',static_url_path='../static')



@forum.errorhandler(404)
def page_not_found(error):
	return render_template('forum/404.html'), 404

@forum.route('/new_post',methods=['GET','POST'])
def new_post():
	if request.method=="POST":
		print("inside the post")
		title=request.form.get("title")
		category=request.form.get("category")
		description=request.form.get("description")
		data={}
		data['title']=title
		data['category']=category
		data['description']=description
		print(data)
		return jsonify(data)



# @forum.route('/')
# def index():
#     print('called')
#     return render_template('forum/home.html')
