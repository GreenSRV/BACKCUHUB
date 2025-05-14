from flask import current_app, jsonify

def success_response(message, status=200):
    return jsonify({"message": message}), status

def error_response(error, status=400):
    return jsonify({"error": str(error)}), status

def get_next_sequence(name):
    counter = current_app.mongo.db.counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return counter["sequence_value"]
def is_unique_student_id(student_id):
        existing_student = current_app.mongo.db.students.find_one({"student_id": student_id})
        return existing_student is None

def is_unique_club_id(club_id):
        existing_club = current_app.mongo.db.clubs.find_one({"club_id": club_id})
        return existing_club is None

def is_unique_club_name(name):
        existing_club = current_app.mongo.db.clubs.find_one({"name": name})
        return existing_club is None