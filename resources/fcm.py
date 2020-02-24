from flask import Flask
from flask import request
from flask_restful import Resource
from Model import db,Users
from pyfcm import FCMNotification
push_service = FCMNotification(api_key="AAAAL3Eegig:APA91bGL-Tvcua23rVfWROEGW_9y8gsFVRNWgdaVcwv2xymYsHqRack5Ege__pD5tN0lriySV2tP35jcQQDaCB-oI4Muc23Q9kKb8hSIXUG4qZODO1j2gUxF1qoyCXDn6liCsv-kPlQo")
class FcmResource(Resource):
    def get(self):
        registration_id = "<device registration_id>"
        message_title = "Uber update"
        message_body = "Hi john, your customized news for today is ready"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)  
        return {'message': result}, 200
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 200
        user=Users.query.filter_by(id=json_data['user_id']).first()
        if user:
            setattr(user, 'deviceid', json_data['deviceid'])
            db.session.commit()
            return {'status': 'success'}, 200
        else:
            return {'status': 'fail'}, 200

        


     



     

        
       

       
