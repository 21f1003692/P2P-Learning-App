from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
swaggerui_blueprint = get_swaggerui_blueprint(
    Config.SWAGGER_URL,
    Config.API_URL,
    config={
        'app_name': 'API Gateway/User Service'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=Config.SWAGGER_URL)
migrate = Migrate(app, db)

from app import routes, models