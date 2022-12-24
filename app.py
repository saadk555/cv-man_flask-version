import io

import os

import sys

from ast import dump

from glob import glob

from io import BytesIO

from zipfile import ZipFile



import flask

import flask_login

from flask import *

from flask import after_this_request, session

from flask_login import *



secret = os.environ.get("PWDS")



users = {'panda@rabbit.com': {'password': 'pandarabbit37424562'}}







UPLOAD_FOLDER = "/home/bluxbeeg/project.pekisa.com/UPLOAD_FOLDER/"

ALLOWED_EXTENSIONS = 'pdf'





app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000

app.secret_key = "uwerhkuweh7"

app.static_folder = 'static'

login_manager = LoginManager()

login_manager.init_app(app)





keyword = []



class User(UserMixin):

    pass





@login_manager.user_loader

def user_loader(email):

    if email not in users:

        return



    user = User()

    user.id = email

    return user





@login_manager.request_loader

def request_loader(request):

    email = request.form.get('email')

    if email not in users:

        return



    user = User()

    user.id = email

    return user







@app.route('/login', methods=['GET', 'POST'])

def login():

    if flask.request.method == 'GET':

        return '''

               <form action='login' method='POST'>

                <input type='text' name='email' id='email' placeholder='email'/>

                <input type='password' name='password' id='password' placeholder='password'/>

                <input type='submit' name='submit'/>

               </form>

               '''



    email = flask.request.form['email']

    if email in users and flask.request.form['password'] == users[email]['password']:

        user = User() 

        user.id = email

        flask_login.login_user(user)

        return flask.redirect('/')



    return "Sorry, login failed :("





@app.route('/logout')

def logout():

    flask_login.logout_user()

    return 'You have been succcessfully logged out'





@app.route('/protected')

@flask_login.login_required

def protected():

    return 'You are logged in as: ' + flask_login.current_user.id



@app.route('/')  

@login_required

def index(): 

    return render_template("index.html")  



@app.route('/success', methods = ['POST'])  

@login_required

def success():  

    if request.method == 'POST':  

        key = request.form['k']  

        return render_template("keywords.html", number = int(key))  







@app.route('/submitted', methods = ['POST'])

@login_required

def submitted():

    if request.method == 'POST':

        return render_template("result.html")


@app.route('/file', methods = ['GET'])

@login_required

def file():

    if request.method == 'GET':

        return send_file('result\\result.pdf', mimetype='application/pdf', download_name='result.pdf')

        

        



@login_manager.unauthorized_handler

def unauthorized_handler():

    return 'Unauthorized, Please visit https://project.pekisa.com/login'



    



if __name__ == '__main__':  

    app.run(host= '0.0.0.0', debug = True) 

