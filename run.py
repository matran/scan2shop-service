from flask import Flask
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    from Model import db
    from resources.auth import mail
    mail.init_app(app)
    db.init_app(app)
    return app
if __name__ == "__main__":
    app = create_app("config")
    app.debug = True
    #app.run()
    app.run(host = '0.0.0.0',port=80)