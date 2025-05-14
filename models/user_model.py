from marshmallow import Schema, fields

class StudentSchema(Schema):
    _id = fields.Str(dump_only=True)
    student_id = fields.Str(required=True)
    name = fields.Str(required=True)
    year = fields.Int(required=True)

class ClubSchema(Schema):
    _id = fields.Str(dump_only=True)
    club_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    date = fields.Str(required=True)
    faculty = fields.Str(required=True)
    image = fields.Str(required=True)
    members = fields.Int(required=True)
