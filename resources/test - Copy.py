from flask_restful import Resource
from flask import url_for
from flask import jsonify
import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config.from_object('config')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
class TestResource(Resource):
    def get(self):
        url=url_for('api.callbackresource',_external=True)
        return {'url':url}, 200
    def delete(self):
        json_data = request.get_json(force=True)
        url=json_data['urlpath'];
        file= url.rsplit('/', 1)[-1]
        myfile=os.path.join(app.config['UPLOAD_FOLDER'], file)
        try:
            os.remove(myfile)
        except OSError as e:  ## if failed, report it back to the user ##
            #print ("Error: %s - %s." % (e.filename, e.strerror))
             return { "status": 'success','message':"Error: %s - %s." % (e.filename, e.strerror)}, 200
    def post(self):
    
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        barcode=request.form['barcode']
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl=request.host_url+'static/'+filename
            resp = jsonify({'message' : 'File successfully uploaded','url':barcode})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
