from flask import request
from flask import Flask
from flask_mail import Mail
from flask_restful import Resource
from flask_mail import Message
import secrets
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime, timedelta
from flask import current_app
from flask_restful import Api
from flask import flash
from flask import url_for
from flask import jsonify
from forms import ResetPasswordForm
from flask import render_template,make_response
from Model import db, Users,UserSchema,PasswordChange
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
user_schema = UserSchema()
users_schema=UserSchema(many=True)
app = Flask(__name__)
app.config.from_object('config')
mail = Mail()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
class AuthUsersResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status':'fail','message': 'No input data provided'}, 200
        user = Users.query.filter_by(email=json_data['email']).first()
        if user:
            return {'status':'fail','message': 'User already exists'}, 200
        user = Users(
            firstname=json_data['firstname'],
            lastname=json_data['lastname'],
            phone=json_data['phone'],
            email=json_data['email'],
            password=generate_password_hash(json_data['password'], method='sha256'),
            privilege=json_data['privilege']
            )
        db.session.add(user)
        db.session.commit()
        result ="saved successfully"
        return { 'status': 'success','message':'register successful', 'data': result }, 200
    def get(self):
        users = Users.query.filter_by(privilege="user").all()
        users = users_schema.dump(users)
        return jsonify(users)
    def delete(self,id):
        user = Users.query.filter_by(id=id).delete()
        db.session.commit()
        if user:
            return { "status": 'success'}, 200
        else:
            return { "status": 'fail'}, 200
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status': 'fail','message': 'No input data provided'}, 200
        user = Users.query.filter_by(id=json_data['id']).first()
        if not user:
            return {'status': 'fail','message': 'User does not exist'}, 200
        user.firstname = json_data['firstname']
        user.lastname=json_data['lastname']
        user.phone=json_data['phone']
        user.email=json_data['email']
        db.session.commit()
        return { 'status': 'success','message':'successfully updated'}, 200  
class PackagerResource(Resource):
    def get(self):
        users = Users.query.filter_by(privilege="packager").all()
        users = users_schema.dump(users)
        return jsonify(users)
class ProfilePhotoResource(Resource):
    def post(self):
        userid=request.form['userid']
        photo= request.files['pic']
        user = Users.query.filter_by(id=userid).first()
        if not user:
            return {'status': 'fail','message': 'User does not exist'}, 200
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], "profile_"+userid+"_"+filename))
            fileurl=request.host_url+'static/'+"profile_"+userid+"_"+filename
            user.photo=fileurl
            db.session.commit()
            return { "status": 'success','message':'uploaded successfully','url':fileurl}, 200
        else:
            resp = jsonify({'status':'fail','message' : 'Wrong file type ensure you are uploading image'})
            resp.status_code = 200
            return resp


class AuthLoginResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status':'fail','message': 'No input data provided'}, 200
        user = Users.query.filter_by(email=json_data['email'],privilege=json_data['privilege']).first()
        if not user or not check_password_hash(user.password, json_data['password']):
            return {'status':'fail','message': 'Wrong email or password'}, 200
        if user and check_password_hash(user.password,json_data['password']):
            access_token = user.generate_token(user.id)
            if access_token:
                user = user_schema.dump(user)
                result =access_token.decode()
                return { "status": 'success','message':'login successful', 'token': result,'data':user }, 200
class PasswordChangeResource(Resource):
    def get(self,email):
        user = Users.query.filter_by(email=email).first()
        #tomorrow = func.dateadd(func.now(), text('interval 1 day'))
        created = datetime.now() + timedelta(days=1)
        if user:
            token=secrets.token_urlsafe(20)
            pcr = PasswordChange(token=token,email=email,expires=created)
            db.session.add(pcr)
            db.session.commit()
            send_password_reset_email(user,token)
            return {'status': 'success'}, 200
        else:
            return {'status': 'fail'}, 200

            
class PasswordResetResource(Resource):
    def get(self,token):
        headers = {'Content-Type': 'text/html'}
        form = ResetPasswordForm()
        if form.validate_on_submit():
            #user.set_password(form.password.data)
            #db.session.commit()
            updatePassword(token,form.password.data)
            flash('Your password has been reset.')
        return make_response(render_template('reset_password.html',form=form),200,headers)
    def post(self,token):
        headers = {'Content-Type': 'text/html'}
        form = ResetPasswordForm()
        if form.validate_on_submit():
            #user.set_password(form.password.data)
            #db.session.commit()
            updatePassword(token,form.password.data)
            
        return make_response(render_template('reset_password.html',form=form),200,headers)
def updatePassword(token,password):
    currentdate = datetime.now()
    passwordchange=db.session.query(PasswordChange).filter(PasswordChange.token==token,PasswordChange.expires>=currentdate).first()
    #passwordchange=PasswordChange.query.filter_by(token=token,expires=>currentdate).first()  
    if passwordchange:
        email=passwordchange.email
        user=Users.query.filter_by(email=email).first()
        if user:
            pwd=generate_password_hash(password, method='sha256')
            setattr(user, 'password', pwd)
            db.session.commit()
            flash('Your password has been reset.')
    else:
        flash('Link has expired')

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
def send_password_reset_email(user,token):
    url=url_for('api.passwordresetresource', token=token,_external=True)
    send_email('[Scan2Shop] Reset Your Password',sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, url=url),
               html_body=render_template('email/reset_password.html',
                                         user=user, url=url))
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

