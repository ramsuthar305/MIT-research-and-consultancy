from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
from flask import session
import hashlib
from bson.json_util import dumps
import json
from datetime import datetime
# custom imports
from .models import Forum_model
from bson import ObjectId


forum_obj = Forum_model()

forum = Blueprint("forum", __name__, template_folder='../template',
                  static_folder='../static', static_url_path='../static')


@forum.errorhandler(404)
def page_not_found(error):
    return render_template('forum/404.html'), 404


@forum.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == "POST":
        print("inside the post")
        data_received=request.get_data()
        data_received=data_received.decode("utf-8")
        data_received=json.loads(data_received)
        print(type(data_received))
        title = data_received["title"].capitalize()
        category = data_received["category"]
        description = data_received["description"]
        created_on = datetime.now()
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['title'] = title
        data['category'] = category
        data['description'] = description
        data['created_on'] = created_on
        data['uid'] = uid
        data['answers'] = []
        data['upvotes'] = []
        data['downvotes'] = []
        data['reports'] = []
        result = forum_obj.new_post(data)
        return_data={}
        if result!=False:
            return_data['status']=True
            return_data['data']=result
        else:
            return_data['status']=False
            return_data['data']=None
        print("this is result: ", return_data)
        return dumps(return_data)


@forum.route('/new_answer', methods=['GET', 'POST'])
def new_answer():
    if request.method == "POST":
        print("inside the post")
        answer = request.form.get("answer")
        created_on = datetime.now()
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['answer'] = answer
        data['_id'] = ObjectId()
        data['created_on'] = created_on
        data['uid'] = uid
        data['comments'] = []
        data['upvotes'] = []
        data['downvotes'] = []
        data['reports'] = []
        result = forum_obj.new_answer(data, "5eee171819f4780a00e54d0d")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_upvote', methods=['GET', 'POST'])
def new_upvote():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['uid'] = uid
        result = forum_obj.new_upvote(data, "5eee171819f4780a00e54d0d")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_downvote', methods=['GET', 'POST'])
def new_downvote():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['uid'] = uid
        result = forum_obj.new_downvote(data, "5eee171819f4780a00e54d0d")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_report', methods=['GET', 'POST'])
def new_report():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        report = request.form.get("report")
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['_id'] = ObjectId()
        data['uid'] = uid
        data['report'] = report
        result = forum_obj.new_report(data, "5eee171819f4780a00e54d0d")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_comment', methods=['GET', 'POST'])
def new_comment():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        comment = request.form.get("comment")
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['_id'] = ObjectId()
        data['uid'] = uid
        data['comment'] = comment
        result = forum_obj.new_comment(
            data, "5eee171819f4780a00e54d0d", "5eee1c5b7e6b169efa66a58f")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_answer_report', methods=['GET', 'POST'])
def new_answer_report():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        report = request.form.get("report")
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['_id'] = ObjectId()
        data['uid'] = uid
        data['report'] = report
        result = forum_obj.new_answer_report(
            data, "5eee171819f4780a00e54d0d", "5eee1c5b7e6b169efa66a58f")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_answer_upvote', methods=['GET', 'POST'])
def new_answer_upvote():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['uid'] = uid
        result = forum_obj.new_answer_upvote(
            data, "5eee171819f4780a00e54d0d", "5eee1c5b7e6b169efa66a58f")
        print("this is result: ", result)
        return dumps(result)


@forum.route('/new_answer_downvote', methods=['GET', 'POST'])
def new_answer_downvote():
    if request.method == "POST":
        print("inside the post")
        created_on = datetime.now()
        uid = "ramsuthar305@gmail.com"
        data = {}
        data['created_on'] = created_on
        data['uid'] = uid
        result = forum_obj.new_answer_downvote(
            data, "5eee171819f4780a00e54d0d", "5eee1c5b7e6b169efa66a58f")
        print("this is result: ", result)
        return dumps(result)

@forum.route('/delete_post', methods=["GET", "POST"])
def delete_post():
    post_id = "5eee2e3ecfd6bc8710d6df93"
    result = forum_obj.delete_post(post_id)
    print("this is result: ", result)
    return dumps(result)


@forum.route('/delete_answer', methods=["GET", "POST"])
def delete_answer():
    post_id = "5eee171819f4780a00e54d0d"
    answer_id = "5eee1c5b7e6b169efa66a58f"
    result = forum_obj.delete_answer(post_id, answer_id)
    print("this is result: ", result)
    return dumps(result)


@forum.route('/delete_comment', methods=["GET", "POST"])
def delete_comment():
    post_id = "5eee171819f4780a00e54d0d"
    answer_id = "5eee1c5b7e6b169efa66a58f"
    comment_id = "5eee2c1672ca19fbc3fdba0d"
    result = forum_obj.delete_comment(post_id, answer_id, comment_id)
    print("this is result: ", result)
    return dumps(result)

@forum.route('/')
def index():
    print('called')
    return render_template('forum/home.html',posts=forum_obj.get_all_posts())
