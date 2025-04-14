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
