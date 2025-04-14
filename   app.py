from flask import Blueprint, Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_cors import CORS
import os
import certifi
from routes.user_routes import user_bp

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
# Initialize MongoClient with certifi
mongo = PyMongo(app, tlsCAFile=certifi.where())
app.mongo = mongo
print("Connected to MongoDB!")
app.register_blueprint(user_bp)

# Debug route to show collections

############### 
if __name__ == '__main__':
    print("Starting Flask app... YYY")
    print("Mongo URI:", os.getenv("MONGO_URI")) 
    app.run(debug=True)