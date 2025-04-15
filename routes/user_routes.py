from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from bson.json_util import dumps
from models.user_model import StudentSchema, ClubSchema
from utils.response import get_next_sequence, is_unique_club_id, is_unique_student_id, success_response, error_response


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
        #data["student_id"] = get_next_sequence("student_id")  # Auto-increment student_id
        validated = student_schema.load(data)
        if (is_unique_student_id(validated["student_id"]) == False):
            return error_response("Student ID already exists", 400)
        current_app.mongo.db.students.insert_one(validated)
        
        return success_response("Student added successfully", 201)
    except Exception as e:
        return error_response(e, 500)
    
@user_bp.route('/students', methods=['GET'])
def get_students():
    try:
        # Check if query parameter is provided
        search_query = request.args.get('query','')    
        data = current_app.mongo.db.students.find({
            "student_id": {"$regex": search_query, "$options": "i"}
        })
        return dumps(data), 200
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/students/<id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.json
        validated = student_schema.load(data, partial=True)
        # Check if student_id is unique
        # if "student_id" in validated and not is_unique_student_id(validated["student_id"]):
        #     return error_response("Student ID already exists", 400)
        if "student_id" in validated:
            del validated["student_id"] 
            return error_response("Student ID cannot be updated", 400)
        current_app.mongo.db.students.update_one({"student_id": str(id)}, {"$set": validated})
        return success_response("Student updated successfully") 
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    try:
        current_app.mongo.db.students.delete_one({"student_id": str(id)})
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return error_response(e, 500)

# CRUD for ClubSchema
@user_bp.route('/clubs', methods=['POST'])
def add_club():
    try:
        data = request.json
        # data["club_id"] = get_next_sequence("club_id")  # Auto-increment club_id
        validated = club_schema.load(data)
        # Check if club_id is unique
        if (is_unique_club_id(validated["club_id"]) == False):
            return error_response("Club ID already exists", 400)

        current_app.mongo.db.clubs.insert_one(validated)

        return success_response("Club added successfully", 201)
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/clubs', methods=['GET'])
def get_clubs():
    try:
        # Check if query parameter is provided
        search_query = request.args.get('query', '')
        data = current_app.mongo.db.clubs.find({
            "club_id": {"$regex": search_query, "$options": "i"}
        })
        return dumps(data), 200
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/clubs/<id>', methods=['PUT'])
def update_club(id):
    try:
        data = request.json
        validated = club_schema.load(data, partial=True)
        # Check if club_id is unique 
        # if "club_id" in validated and not is_unique_club_id(validated["club_id"]):
        #     return error_response("Club ID already exists", 400)
        if "club_id" in validated:
            del validated["club_id"]  # Prevent updating the club_id
            return error_response("Club ID cannot be updated", 400)
        current_app.mongo.db.clubs.update_one({"club_id": str(id)}, {"$set": validated})
        return success_response("Club updated successfully")
    except Exception as e:
        return error_response(e, 500)
  
@user_bp.route('/clubs/<id>', methods=['DELETE'])
def delete_club(id):
    try:
        current_app.mongo.db.clubs.delete_one({"club_id": str(id)})   
        
        # Remove the club from the students collection
        return jsonify({"message": "Club deleted successfully"}), 200
    except Exception as e:
        return error_response(e, 500)
    


