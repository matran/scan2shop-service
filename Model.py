from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import jwt
app = Flask(__name__)
app.config.from_object('config')
from datetime import datetime, timedelta
ma = Marshmallow()
db = SQLAlchemy()
class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100)) 
    phone = db.Column(db.String(12))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    deviceid=db.Column(db.Text())
    privilege=db.Column(db.String(20))
    def __init__(self,firstname,lastname,phone,email,password,privilege):
        self.firstname=firstname
        self.lastname=lastname
        self.phone=phone
        self.email=email
        self.password=password
        self.privilege=privilege
 
    def generate_token(self,user_id):
       
        try:
            payload={
           
                 'iat':datetime.utcnow(),
                 'sub':user_id
            }
            jwt_string=jwt.encode(payload,app.config['SECRET_KEY'],algorithm='HS256')
            return jwt_string
        except Exception as e:
            return str(e)
    @staticmethod
    def decode_token(token):
        
        try:

            options = {
            'require_exp': False
            }
            payload=jwt.decode(token,app.config['SECRET_KEY'],options=options)
            return payload['sub']

        except jwt.InvalidTokenError:
            return "Invalid token"


class PasswordChange(db.Model):
    __tablename__='password_changes'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text())
    email=db.Column(db.String(100))
    date=db.Column(db.DateTime(timezone=True),server_default=func.now())
    expires=db.Column(db.DateTime(timezone=True))
    def __init__(self,token,email,expires):
        self.token=token
        self.email=email
        self.expires=expires

class Products(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True) 
    barcode = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    description=db.Column(db.String(1000))
    price=db.Column(db.Integer)
    image=db.Column(db.Text())
    def __init__(self,barcode,name,description,price,image):
        self.barcode=barcode
        self.name=name
        self.description=description
        self.price=price
        self.image=image
class ReceiptsTemp(db.Model):
    __tablename__='receipts_temp'
    id = db.Column(db.Integer, primary_key=True)
    receiptid=db.Column(db.Text())
    barcode=db.Column(db.String(13))
    phoneno=db.Column(db.String(13)) 
    name = db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Integer)
    amount=db.Column(db.Integer)
    totalquantity=db.Column(db.Integer)
    def __init__(self,receiptid,barcode,phoneno,name,price,quantity,amount,totalquantity):
        self.receiptid=receiptid
        self.barcode=barcode
        self.phoneno=phoneno
        self.name=name
        self.quantity=quantity
        self.price=price
        self.amount=amount
        self.totalquantity=totalquantity

class Receipts(db.Model):
    __tablename__='receipts'
    id = db.Column(db.Integer, primary_key=True) 
    receiptid=db.Column(db.Text())
    barcode=db.Column(db.String(13))
    date=db.Column(db.DateTime(),server_default=datetime.now().strftime("%Y-%m-%d, %H:%M"))
    phoneno=db.Column(db.String(13)) 
    name = db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Integer)
    amount=db.Column(db.Integer)
    totalquantity=db.Column(db.Integer)
    def __init__(self,receiptid,barcode,phoneno,name,price,quantity,amount,totalquantity):
        self.receiptid=receiptid
        self.barcode=barcode
        self.phoneno=phoneno
        self.name=name
        self.price=price
        self.quantity=quantity
        self.amount=amount
        self.totalquantity=totalquantity

class Feedback(db.Model):
    __tablename__='feedback'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    subject = db.Column(db.String(300)) 
    message = db.Column(db.Text()) 
    def __init__(self,email,subject,message):
        self.email=email
        self.subject=subject
        self.message=message
class ReceiptsSchema(ma.Schema):
    receiptid=fields.String(required=True)
    barcode=fields.String(required=True)
    date=fields.String(required=True)
    phoneno=fields.String(required=True)
    name=fields.String(required=True)
    quantity=fields.Integer()
    price=fields.Integer()
    amount=fields.Integer()
    totalquantity=fields.Integer()

class HistorySchema(ma.Schema):
    barcode=fields.String(required=True)
    date=fields.String(required=True)
    amount=fields.Integer()
    totalquantity=fields.Integer()
    receiptid=fields.String(required=True)



class ProductsSchema(ma.Schema):
    id=fields.Integer()
    barcode=fields.Integer()
    name=fields.String(required=True)
    description=fields.String(required=True)
    price=fields.Integer()
    image=fields.String(required=True)
    
class UserSchema(ma.Schema):
    id=fields.Integer()
    firstname=fields.String(required=True)
    lastname=fields.String(required=True)
    phone=fields.String(required=True)
    email=fields.String(required=True)
   
