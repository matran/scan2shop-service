from flask import request
from flask_restful import Resource
from flask import jsonify
from Model import db,Products,ProductsSchema,Users
from werkzeug.utils import secure_filename
import os
import urllib.request
from flask import Flask, flash, redirect, render_template
app = Flask(__name__)
app.config.from_object('config')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
class ProductResource(Resource):
    def get(self,barcode_id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = Users.decode_token(access_token)
          
            if not isinstance(user_id, str):
                product = Products.query.filter_by(barcode=barcode_id).first()
                if product:
                    product = product_schema.dump(product)
                    return {'status': 'success', 'item':   product}, 200
                else:
                    return {'status':'fail','message':'product not found'},200
            else:
                return {'status':'fail','message':user_id},200
    def post(self):
        #headers = {'Content-Type': 'multipart/form-data'}
        barcode=request.form['barcode']
        file = request.files['file']
        product = Products.query.filter_by(barcode=barcode).first()
        if product:
            return {'status':'fail','message': 'product with same barcode exists'}, 200
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl=request.host_url+'static/'+filename
            product = Products(
            barcode=request.form.get('barcode'),
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=request.form.get('price'),
            image=fileurl
            )
            db.session.add(product)
            db.session.commit()
            return { "status": 'success','message':'successful'}, 200
        else:
            resp = jsonify({'status':'fail','message' : 'Wrong file type ensure you are uploading image'})
            resp.status_code = 200
            return resp
      
    def delete(self,id,url):
        if url!="null":   
            myfile=os.path.join(app.config['UPLOAD_FOLDER'], url)
            try:
                os.remove(myfile)
            except OSError as e:
                print ("Error: %s - %s." % (e.filename, e.strerror))
                #return { "status": 'success','message':"Error: %s - %s." % (e.filename, e.strerror)}, 200
        user = Products.query.filter_by(id=id).delete()
        db.session.commit()
        if user:
            return { "status": 'success'}, 200
        else:
            return { "status": 'fail'}, 200
    def get(self):
        products = Products.query.all()
        products = products_schema.dump(products)
        return jsonify(products)
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status': 'fail','message': 'No input data provided'}, 200
        item = Products.query.filter_by(id=json_data['id']).first()
        if not item:
            return {'status': 'fail','message': 'product does not exist'}, 200
        item.barcode=json_data['barcode'],
        item.name=json_data['name'],
        item.description=json_data['description'],
        item.price=json_data['price'],
        item.image=json_data['image']
        db.session.commit()
        return { 'status': 'success','message':'successfully updated'}, 200   

class ProductResourceOption(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'status':'fail','message': 'No input data provided'}, 200
        product = Products.query.filter_by(barcode=json_data['barcode']).first()
        if product:
            return {'status':'fail','message': 'product with same barcode exists'}, 200
        product = Products(
            barcode=json_data['barcode'],
            name=json_data['name'],
            description=json_data['description'],
            price=json_data['price'],
            image=""
            )
        db.session.add(product)
        db.session.commit()
        return { "status": 'success','message':'successful'}, 200
    def put(self):
        id=request.form['id']
        file = request.files['file']
        imagename=request.form['imagename']
        if imagename!="null":   
            myfile=os.path.join(app.config['UPLOAD_FOLDER'], imagename)
            try:
                os.remove(myfile)
            except OSError as e:
                print ("Error: %s - %s." % (e.filename, e.strerror))
        item = Products.query.filter_by(id=id).first()
        if not item:
            return {'status': 'fail','message': 'product does not exist'}, 200
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl=request.host_url+'static/'+filename
            item.barcode=request.form.get('barcode'),
            item.name=request.form.get('name'),
            item.description=request.form.get('description'),
            item.price=request.form.get('price'),
            item.image=fileurl
            db.session.commit()
            return { "status": 'success','message':'successfully updated'}, 200
        else:
            resp = jsonify({'status':'fail','message' : 'Wrong file type ensure you are uploading image'})
            resp.status_code = 200
            return resp
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

      
