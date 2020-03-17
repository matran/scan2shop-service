from flask import request
from flask import Flask
from flask_restful import Resource
from authy.api import AuthyApiClient
app = Flask(__name__)
app.config.from_object('config')
api = AuthyApiClient(app.config['AUTHY_API_KEY'])
from flask import jsonify
country_code="+254"
class PhoneResource(Resource):
    def get(self,phoneno):
        method="sms"
        res=api.phones.verification_start(phoneno, country_code, via=method)
        if res.ok():
            return { 'status': 'success'}, 200
        else:
            return { 'status': 'fail'}, 200
    def post(self):
        json_data = request.get_json(force=True)
        token=json_data["token"]
        phone_number=json_data["phone"]
        verification = api.phones.verification_check(phone_number,country_code,token)
        if verification.ok():
            return { 'status': 'success'}, 200
        else:
            return { 'status': 'fail'}, 200



        
    
    
    
