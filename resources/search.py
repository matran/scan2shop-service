from flask import Flask
from flask import request
from flask_restful import Resource
from Model import db,Products,ProductsSchema,Users
product_schema = ProductsSchema(many=True)

class SearchResource(Resource):
    def get(self,name):
        product=Products.query.filter(Products.name.like('%'+name+'%'))
        product=product.order_by(Products.name).all()
        if product:
            product = product_schema.dump(product)
            return {'status': 'success', 'products':   product}, 200
        else:
            return {'status':'fail','message':'product not found'},200
         

        
       

       
