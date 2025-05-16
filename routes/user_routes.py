from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from bson.json_util import dumps
from models.user_model import StudentSchema, ClubSchema
from utils.response import  is_unique_student_id, success_response, error_response, is_unique_club_name


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


@user_bp.route('/students/login' , methods=['POST'])
def login_student():
    #pass student_id and password from body
    try:
        data = request.json
        student_id = data.get("student_id")
        password = data.get("password")
        club = data.get("club")
        sending = {
            "student_id": student_id,
            "password": password,
            "club": club
        }
        if not student_id or not password:
            return error_response("Student ID and Password are required", 400)
        
        student = current_app.mongo.db.students.find_one({"student_id": student_id, "password": password})
        if student:
            return success_response(("Login successful",sending ), 200)
        else:
            return error_response("Invalid Student ID or Password", 401)
    except Exception as e:
        return error_response(e, 500)
    
    
    
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

@user_bp.route('/students/<id>/addclub', methods=['PUT'])
def add_club_to_student(id):
    try:
        club_name = request.json.get("club")
        if not club_name:
            return error_response("Club name required", 400)
        result = current_app.mongo.db.students.update_one(
            {"student_id": str(id)},
            {"$addToSet": {"club": club_name}}
        )
        if result.matched_count == 0:
            return error_response("Student ID not found", 404)
        if result.modified_count == 0:
            return error_response("Club already added or no change made", 400)

        return success_response("Club added successfully")
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    try:
        current_app.mongo.db.students.delete_one({"student_id": str(id)})
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return error_response(e, 500)



@user_bp.route('/clubs/rating/<id>', methods=['POST'])
def add_student_rating(id):
    try:
        data = request.json
        rating = data.get("rating")
        if not rating or not (1 <= rating <= 5):
            return error_response("Rating must be between 1 and 5", 400)
        
        # Check if student_id exists
        student = current_app.mongo.db.students.find_one({"student_id": str(id)})
        if not student:
            return error_response("Student ID not found", 404)
        current_app.mongo.db.clubs.update_one( {"$push": {"ratings": rating}})
        return success_response("Rating added successfully", 201)
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
        if (is_unique_club_name(validated["name"]) == False):
            return error_response("Club Name already exists", 400)

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
            "name": {"$regex": search_query, "$options": "i"}
        })
        return dumps(data), 200
    except Exception as e:
        return error_response(e, 500)

@user_bp.route('/clubs/<name>', methods=['PUT'])
def update_club(name):
    try:
        data = request.json
        validated = club_schema.load(data, partial=True)
        # Check if club_id is unique 
        # if "club_id" in validated and not is_unique_club_id(validated["club_id"]):
        #     return error_response("Club ID already exists", 400)
        if "name" in validated:
            del validated["name"]  # Prevent updating the club_id
            return error_response("Club Name cannot be updated", 400)
        current_app.mongo.db.clubs.update_one({"name": str(name)}, {"$set": validated})
        return success_response("Club updated successfully")
    except Exception as e:
        return error_response(e, 500)
  
@user_bp.route('/clubs/<name>', methods=['DELETE'])
def delete_club(name):
    try:
        current_app.mongo.db.clubs.delete_one({"name": str(name)})   
        
        # Remove the club from the students collection
        return jsonify({"message": "Club deleted successfully"}), 200
    except Exception as e:
        return error_response(e, 500)
    


