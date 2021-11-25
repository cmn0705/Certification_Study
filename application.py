from flask import Flask, session
from flask_session import Session

application = Flask(__name__)
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)
# -----------------------------------------------------
import index
application.add_url_rule('/',view_func=index.index,methods=['get','post'])

import client_register
application.add_url_rule('/client_register',view_func=client_register.client_register,methods=['get','post'])

import coach_register
application.add_url_rule('/coach_register',view_func=coach_register.coach_register,methods=['get','post'])

import login
application.add_url_rule('/login',view_func=login.login,methods=['get','post'])

import logout
application.add_url_rule('/logout',view_func=logout.logout,methods=['get','post'])

import client_page
application.add_url_rule('/client_page',view_func=client_page.client_page,methods=['get','post'])

import coach_page
application.add_url_rule('/coach_page',view_func=coach_page.coach_page,methods=['get','post'])

import forgot_password
application.add_url_rule('/forgot_password',view_func=forgot_password.forgot_password,methods=['get','post'])

import reset_password
application.add_url_rule('/reset_password/<subject>/<email>/<id>',view_func=reset_password.reset_password,methods=['get','post'])

import practice_aws_cp
application.add_url_rule('/practice_aws_cp',view_func=practice_aws_cp.practice_aws_cp,methods=['get','post'])

import practice_aws_saa
application.add_url_rule('/practice_aws_saa',view_func=practice_aws_saa.practice_aws_saa,methods=['get','post'])

import add_aws_cp
application.add_url_rule('/add_aws_cp',view_func=add_aws_cp.add_aws_cp,methods=['get','post'])

import add_aws_saa
application.add_url_rule('/add_aws_saa',view_func=add_aws_saa.add_aws_saa,methods=['get','post'])

import feedback
application.add_url_rule('/feedback',view_func=feedback.feedback,methods=['get','post'])
# -----------------------------------------------------
if __name__ == "__main__":
    application.run(debug=True, use_reloader=True)