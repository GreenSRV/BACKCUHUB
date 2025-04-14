from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from bson.json_util import dumps
from models.user_model import UserSchema
from utils.response import success_response, error_response


user_bp = Blueprint('user_routes', __name__)
user_schema = UserSchema()

@user_bp.route('/ping')
def index():
    try:
        return "Pong!", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/add', methods=['POST'])
def add():
  
    try:
        data = request.json
        validated = user_schema.load(data)
        current_app.mongo.db.appdevcoll.insert_one(validated)
        return success_response("Added successfully", 201)
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/get', methods=['GET'])
def get():
    data = current_app.mongo.db.appdevcoll.find()
    return dumps(data), 200

@user_bp.route('/update/<id>', methods=['PUT'])
def update(id):
    try:
        data = request.json
        validated = user_schema.load(data, partial=True)  # allow partial updates
        current_app.mongo.db.appdevcoll.update_one({"_id": ObjectId(id)}, {"$set": validated})
        return success_response("Updated successfully")
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    current_app.mongo.db.appdevcoll.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted successfully"}), 200


