from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app) 

@app.route('/add', methods=['POST'])
def add_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    mongo.db.mycollection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/get', methods=['GET'])
def get_data():
    data = mongo.db.mycollection.find()
    return dumps(data), 200

@app.route('/update/<id>', methods=['PUT'])
def update_data(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    mongo.db.mycollection.update_one({"_id": id}, {"$set": data})
    return jsonify({"message": "Data updated successfully"}), 200

@app.route('/delete/<id>', methods=['DELETE'])
def delete_data(id):
    mongo.db.mycollection.delete_one({"_id": id})
    return jsonify({"message": "Data deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)