from flask import Flask
from flask import request
from flask_restful import Resource
from sqlalchemy.sql import text
from Model import db,Users,ReceiptsTemp,Receipts
from mpesa_express import MpesaExpress
from pyfcm import FCMNotification
import random 
import json
import urllib.request
import requests
from sqlalchemy.orm.exc import NoResultFound
push_service = FCMNotification(api_key="AAAAL3Eegig:APA91bGL-Tvcua23rVfWROEGW_9y8gsFVRNWgdaVcwv2xymYsHqRack5Ege__pD5tN0lriySV2tP35jcQQDaCB-oI4Muc23Q9kKb8hSIXUG4qZODO1j2gUxF1qoyCXDn6liCsv-kPlQo")
class PaymentResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status':'fail','message': 'No input data provided'}, 200
        receipt=json_data['receipt']
        rct= json.loads(receipt)
        phone=json_data['phonenumber']
        receiptid=json_data['receiptid']
        totalquantity=json_data['totalquantity']
        barcode=generate_barcode_digit()
        app_key="AwKdEddVt9FXP19meSCAm1O4e7xAeljh"
        app_secret="26EJPoyFn9AG7R35"
        sandbox_url="https://sandbox.safaricom.co.ke"
        live_url="https://api.safaricom.co.ke"
        business_shortcode="954904"
        passcode="063792888642c054b3826dbf5c89dcab7e58cff74c18a8c6ee18d0939c049261"
        amount=json_data['amount']
        phone_number=json_data['phonenumber']
        #callback_url=url=request.host_url+'api/callback'
        callback_url="http://9ddf0863.ngrok.io/api/callback"
        reference_code=json_data['phonenumber']
        description="RANDOM DESCRIPTION"
        rcpts = ReceiptsTemp.query.filter_by(phoneno=phone).first()
        if not rcpts:
            objects = []
            for item in rct:
                objects.append(ReceiptsTemp(receiptid,barcode,phone,item['name'],item['total'],item['quantity'],amount,totalquantity))
            db.session.bulk_save_objects(objects)
            db.session.commit()
            try:
                self.mpesa_express_object = MpesaExpress("production",app_key=app_key, app_secret=app_secret,sandbox_url=sandbox_url,live_url=live_url)
                self.token = self.mpesa_express_object.authenticate()
                response = self.mpesa_express_object.stk_push(business_shortcode=business_shortcode,passcode=passcode,amount=amount,phone_number=phone_number,callback_url=callback_url,reference_code=reference_code,description=description)
            except requests.exceptions.ConnectionError:
                return {'status':'fail','message': "connection error"}, 200
            else:
                return {'status':'success','message': response}, 200
        else:
            rst = ReceiptsTemp.query.filter_by(phoneno=phone).delete()
            db.session.commit()
            objects = []
            for item in rct:
                objects.append(ReceiptsTemp(receiptid,barcode,phone,item['name'],item['total'],item['quantity'],amount,totalquantity))
            db.session.bulk_save_objects(objects)
            db.session.commit()
            try:
                self.mpesa_express_object = MpesaExpress("production",app_key=app_key, app_secret=app_secret,sandbox_url=sandbox_url,live_url=live_url)
                self.token = self.mpesa_express_object.authenticate()
                response = self.mpesa_express_object.stk_push(business_shortcode=business_shortcode,passcode=passcode,amount=amount,phone_number=phone_number,callback_url=callback_url,reference_code=reference_code,description=description)
            except requests.exceptions.ConnectionError:
                return {'status':'fail','message': "connection error"}, 200
            else:
                return {'status':'success','message': response}, 200

class CallBackResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'status':'fail','message': 'No input data provided'}, 200
        try:
            phoneno=json_data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        except KeyError:
            print('payment failed')
            return {'status':'fail','message': 'payment failed'}, 200
        if phoneno:
            try:
                receiptstemp=db.session.query(ReceiptsTemp).filter(ReceiptsTemp.phoneno==str(phoneno))
            except NoResultFound:
                return {'message':'no receipt found'},200
            if receiptstemp.count()>0:
                keys = db.inspect(ReceiptsTemp).columns.keys()
                get_columns = lambda receipts: {key: getattr(receipts, key) for key in keys}
                db.session.bulk_insert_mappings(Receipts, (get_columns(receipts) for receipts in receiptstemp))
                receiptstemp.delete(synchronize_session='fetch')
                #db.session.expire_all()
                db.session.commit()
                user=Users.query.filter_by(phone=str(phoneno)).first()
                
                if user:
                    registration_id = user.deviceid
                    message_title = "Payment successful"
                    message_body = "Mpesa payment successful"
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)  
                    print(result)
                    return {'message': result}, 200
                else:
                    return {'message':'user not found'},200
            else:
                print('payment failed')
                return {'message':'no receipt found'},200
def generate_barcode_digit():
    r1 = random.randint(100000000000, 999999999999) 
    cd=str((10 - sum((3, 1)[i % 2] * int(n) for i, n in enumerate(reversed(str(r1))))) % 10)
    return str(r1)+cd

def sendPushNotification(deviceid,title,message):
    registration_id = deviceid
    message_title = title
    message_body = message
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)  
    return {'message': result}, 200

        






     



     

        
       

       
