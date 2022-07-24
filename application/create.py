from .backend.models import *


username = "Admin"
password = "12345"
level = "Admin"
db.session.add(User(username,password,level))
db.session.commit()