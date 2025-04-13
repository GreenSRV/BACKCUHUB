from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from bson.json_util import dumps

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/add', methods=['POST'])
def add():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    current_app.mongo.db.mycollection.insert_one(data)
    return jsonify({"message": "Added successfully"}), 201

@user_bp.route('/get', methods=['GET'])
def get():
    data = current_app.mongo.db.mycollection.find()
    return dumps(data), 200

@user_bp.route('/update/<id>', methods=['PUT'])
def update(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    current_app.mongo.db.mycollection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Updated successfully"}), 200

@user_bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    current_app.mongo.db.mycollection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted successfully"}), 200
