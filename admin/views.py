from flask import Blueprint, render_template, request, redirect, session, jsonify, flash, url_for, abort
from functools import wraps
import hashlib
import json
from datetime import datetime

#custom imports
from .models import Users, Shortlist
from .models import Jobs
shorlist_obj=Shortlist()
user_object = Users()
jobs=Jobs()
admin = Blueprint("admin", __name__, template_folder='../templates', static_folder='../static/admin',
                   static_url_path='../static/admin')


@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/404.html'), 404

@admin.route('/',methods=['POST','GET'])
def dashboard():
    try:
        return render_template('admin/index.html')
        
    except Exception as error:
        print(error)
        return render_template('admin/index.html')
