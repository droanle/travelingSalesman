from flask import Blueprint
from Src.View.Home import Home
from Src.Controller.Execute import Execute

Router = Blueprint('router', __name__)

Router.register_blueprint(Home)
Router.register_blueprint(Execute)