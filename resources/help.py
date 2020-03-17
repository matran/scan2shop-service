from flask import request
from flask_restful import Resource
from flask import render_template,make_response
class HelpResource(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('help.html'),200,headers)
        
         
