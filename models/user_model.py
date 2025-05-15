from marshmallow import Schema, fields

class StudentSchema(Schema):
    _id = fields.Str(dump_only=True)
    student_id = fields.Str(required=True)
    password = fields.Str(required=True)
    club = fields.List(fields.Str(), missing=[], dump_default=[])

class ClubSchema(Schema):
    _id = fields.Str(dump_only=True)
    club_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    date = fields.Str(required=True)
    faculty = fields.Str(required=True)
    image = fields.Str(required=True)
    members = fields.Str(required=True)
    ratings = fields.List(fields.Int(validate=lambda x: 1 <= x <= 5), missing=[], dump_default=[])
    average_rating = fields.Float(dump_only=True)
    
