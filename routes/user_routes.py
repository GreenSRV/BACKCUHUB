from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from bson.json_util import dumps
from models.user_model import StudentSchema, ClubSchema
from utils.response import get_next_sequence, success_response, error_response

user_bp = Blueprint('user_routes', __name__)
student_schema = StudentSchema()
club_schema = ClubSchema()

# Ping route
@user_bp.route('/ping')
def index():
    try:
        return "Pong!", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CRUD for StudentSchema
@user_bp.route('/students', methods=['POST'])
def add_student():
    try:
        data = request.json
        data["student_id"] = get_next_sequence("student_id")  # Auto-increment student_id
        validated = student_schema.load(data)
        current_app.mongo.db.students.insert_one(validated)
        return success_response("Student added successfully", 201)
    except Exception as e:
        return error_response(e, 500)
    
@user_bp.route('/students', methods=['GET'])
def get_students():
    try:
        data = current_app.mongo.db.students.find()
        return dumps(data), 200
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/students/<id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.json
        validated = student_schema.load(data, partial=True)
        current_app.mongo.db.students.update_one({"_id": ObjectId(id)}, {"$set": validated})
        return success_response("Student updated successfully")
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    try:
        current_app.mongo.db.students.delete_one({"student_id": int(id)})
        if current_app.mongo.db.students.deleted_count == 0:
            return error_response("Student not found", 404)
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return error_response(e, 500)

# CRUD for ClubSchema
@user_bp.route('/clubs', methods=['POST'])
def add_club():
    try:
        data = request.json
        data["club_id"] = get_next_sequence("club_id")  # Auto-increment club_id
        validated = club_schema.load(data)
        current_app.mongo.db.clubs.insert_one(validated)
        return success_response("Club added successfully", 201)
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/clubs', methods=['GET'])
def get_clubs():
    try:
        data = current_app.mongo.db.clubs.find()
        return dumps(data), 200
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/clubs/<id>', methods=['PUT'])
def update_club(id):
    try:
        data = request.json
        validated = club_schema.load(data, partial=True)
        current_app.mongo.db.clubs.update_one({"_id": ObjectId(id)}, {"$set": validated})
        return success_response("Club updated successfully")
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/clubs/<id>', methods=['DELETE'])
def delete_club(id):
    try:
        current_app.mongo.db.clubs.delete_one({"student_id " : int(id)})   
        if current_app.mongo.db.clubs.deleted_count == 0:
            return error_response("Club not found", 404)
        # Remove the club from the students collection
        return jsonify({"message": "Club deleted successfully"}), 200
    except Exception as e:
        return error_response(e, 500)
    


