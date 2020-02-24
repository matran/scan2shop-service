import os

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://pfjvpvkxnewmbb:500f424b84de714cb65e0128880fa098577a5d0629c834f3e2407319455cf68e@ec2-18-210-51-239.compute-1.amazonaws.com:5432/ddgrf8kj6euol6"
#SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:henry5765@localhost/flaskapp"
SECRET_KEY ="\xbfK\xcf\xbf\xb4 \x83\xfa\xd8W\xd1Ey\xba\xc4\xd0\x1e\xe5\xb7m\xef_\xe0\x1a"
ADMINS = 'matranic@gmail.com'
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587  
MAIL_USE_TLS=1
MAIL_USERNAME='matranic@gmail.com'
MAIL_PASSWORD='Divine*henry123'
UPLOAD_FOLDER='./static'