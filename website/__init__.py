from flask import Flask,Blueprint
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_ckeditor import CKEditor


db=MySQL()
mail=Mail()
ckeditor=CKEditor()


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='MIZAN'
    UPLOAD_FOLDER = '/home/zeus/tasfia_israt_final_project/website/static/file'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3'}

    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'interior_design_and_shop'

    app.config["MAIL_SERVER"]='smtp.gmail.com' 
    app.config["MAIL_PORT"] = 465
    app.config['MAIL_USE_TLS'] = False  
    app.config['MAIL_USE_SSL'] = True  
    app.config["MAIL_USERNAME"] = 'dekbovideo@gmail.com'  
    app.config['MAIL_PASSWORD'] = '5255452554'  

    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)

    from .auth import auth
    from .interior import interior
    from .admin import admin
    from .shop import shop

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(interior, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(shop, url_prefix="/")

    return app
