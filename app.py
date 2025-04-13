from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

from config.config import Config
from routes.user_routes import user_bp

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = Config.MONGO_URI
mongo = PyMongo(app)
app.mongo = mongo  # Attach Mongo to app for reuse

app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(host="http://127.0.0.1:5000", port=5000, debug=True)
    
