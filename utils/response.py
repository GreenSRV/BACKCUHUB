from flask import jsonify

def success_response(message, status=200):
    return jsonify({"message": message}), status

def error_response(error, status=400):
    return jsonify({"error": str(error)}), status
