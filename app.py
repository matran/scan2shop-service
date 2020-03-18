from flask import Blueprint
from flask_restful import Api
from resources.auth import AuthUsersResource,AuthLoginResource,PasswordChangeResource,PasswordResetResource,PackagerResource, ProfilePhotoResource
from resources.products import ProductResource,ProductResourceOption
from resources.search import SearchResource
from resources.fcm import FcmResource
from resources.receipts import ReceiptsResource,HistoryResource,InvoiceResource,ReceiptResource,RecentReceiptResource
from resources.payment import PaymentResource, CallBackResource
from resources.feedback import FeedBackResource
from resources.test import TestResource
from resources.phoneverify import PhoneResource
from resources.help import HelpResource
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
# Route
api.add_resource(HelpResource,'/help')
api.add_resource(ProfilePhotoResource,'/uploadphoto')
api.add_resource(PhoneResource,'/verify','/phone/<string:phoneno>')
api.add_resource(TestResource,'/test')
api.add_resource(RecentReceiptResource,'/resent/<string:phoneno>')
api.add_resource(AuthUsersResource,'/users','/users/<string:id>')
api.add_resource(PackagerResource,'/packager')
api.add_resource(AuthLoginResource,'/login')
api.add_resource(ProductResource, '/products/<string:barcode_id>','/products','/product/<int:id>/<string:url>')
api.add_resource(SearchResource,'/search/<string:name>')
api.add_resource(ProductResourceOption,'/productsoption')
api.add_resource(FcmResource,'/fcm')
api.add_resource(PaymentResource,'/payment')
api.add_resource(CallBackResource,'/callback')
api.add_resource(ReceiptResource,'/receipt/<string:receiptid>','/receipts')
api.add_resource(ReceiptsResource,'/receipt')
api.add_resource(HistoryResource,'/history/<string:phoneno>')
api.add_resource(InvoiceResource,'/invoice/<string:barcode>')
api.add_resource(FeedBackResource,'/feedback')
api.add_resource(PasswordChangeResource,'/passwordrequest/<string:email>')
api.add_resource(PasswordResetResource,'/passwordreset/<string:token>')