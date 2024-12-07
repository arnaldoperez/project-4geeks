  
import os
from flask_admin import Admin
from .models import db, User,TokenBlockedList
from flask_admin.contrib.sqla import ModelView, BaseModelView

def InjectModelView(BaseClass):
    return BaseModelView(BaseClass)

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')


    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session, column_exclude_list=None))
    admin.add_view(ModelView(TokenBlockedList, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))