from flask import Flask
from models.user_model import user_model
app = Flask(__name__)
app.debug =True

try:
    from controllers import user_controller
except Exception as e:
    print(e)

