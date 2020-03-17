from flask import request
from flask_restful import Resource
from Model import db, Receipts, ReceiptsSchema,HistorySchema
from sqlalchemy.sql import text
from sqlalchemy import distinct
from flask import jsonify
import json
from sqlalchemy import func
receipts_schema = ReceiptsSchema(many=True)
receipt_schema = ReceiptsSchema()
history_schema=HistorySchema(many=True)
class ReceiptResource(Resource):
    def get(self,receiptid):
        receipt=Receipts.query.filter_by(receiptid=receiptid)
        receipts= receipts_schema.dump(receipt)
        return {'status': 'success', 'receipt': receipts}, 200
    
class ReceiptsResource(Resource):
    def get(self):
        receipts = Receipts.query.all()
        receipts = receipts_schema.dump(receipts)
        return jsonify(receipts)

class HistoryResource(Resource):
    def get(self,phoneno):
        receipt=Receipts.query.filter_by(phoneno=str(phoneno)).distinct(Receipts.date)
        receipts= history_schema.dump(receipt)
        return {'status': 'success', 'history': receipts}, 200
class InvoiceResource(Resource):
     def get(self,barcode):
        receipt=Receipts.query.filter_by(barcode=str(barcode))
        receipts= receipts_schema.dump(receipt)
        return {'status': 'success', 'receipt': receipts}, 200
class RecentReceiptResource(Resource):
    def get(self,phoneno):
        receipt=Receipts.query.filter(Receipts.phoneno==str(phoneno)).order_by(Receipts.date.desc()).first()
        if receipt:
            receipts= receipt_schema.dump(receipt)
            date=receipts['date']
            receipt=Receipts.query.filter(Receipts.phoneno==str(phoneno)).filter(Receipts.date==date)
            if receipt:
                receipts= receipts_schema.dump(receipt)
                return {'status': 'success', 'receipt': receipts}, 200
            else:
                return {'status': 'fail','receipt':[]}, 200
        else:
            return {'status': 'fail','receipt':[]}, 200
            
    
    
