import os

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://yjmeixtqsoxpyv:da5156c6578aff52851cf14d749ddb9c6a3403f0e748afce6979181fe49dc794@ec2-18-233-137-77.compute-1.amazonaws.com:5432/ddkfu1dug68ind"
#SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:henry5765@localhost/flaskapp"
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:henry5765@localhost/scan2shop"
SECRET_KEY ="\xbfK\xcf\xbf\xb4 \x83\xfa\xd8W\xd1Ey\xba\xc4\xd0\x1e\xe5\xb7m\xef_\xe0\x1a"
ADMINS = 'matranic@gmail.com'
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587  
MAIL_USE_TLS=1
MAIL_USERNAME='matranic@gmail.com'
MAIL_PASSWORD='Divine*power123'
UPLOAD_FOLDER='./static'
AUTHY_API_KEY = '5NWHaP7ZVYQjp66bMpiM16DfXkeJCnw8'
