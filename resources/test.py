from flask_restful import Resource
from flask import url_for
from flask import jsonify
from pyfcm import FCMNotification
import random 
import json
import requests
from Model import db,Users,ReceiptsTemp,Receipts
from flask import request
from flask_restful import Resource
from flask import jsonify
from Model import db,Products,ProductsSchema,Users
from werkzeug.utils import secure_filename
import os
import urllib.request
push_service = FCMNotification(api_key="AAAAL3Eegig:APA91bGL-Tvcua23rVfWROEGW_9y8gsFVRNWgdaVcwv2xymYsHqRack5Ege__pD5tN0lriySV2tP35jcQQDaCB-oI4Muc23Q9kKb8hSIXUG4qZODO1j2gUxF1qoyCXDn6liCsv-kPlQo")
class TestResource(Resource):
    def get(self):
        url=request.host_url+'api/callback'
        return {'message': url}, 200
        
