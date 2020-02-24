from flask import request
from flask_restful import Resource
from Model import db, Feedback

class FeedBackResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status': 'fail'}, 200
        feedback = Feedback(
            email=json_data['email'],
            subject=json_data['subject'],
            message=json_data['message']
            )
        db.session.add(feedback)
        db.session.commit()
        return { "status": 'success' }, 200
     
