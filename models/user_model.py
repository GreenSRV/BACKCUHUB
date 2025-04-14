from marshmallow import Schema, fields

class StudentSchema(Schema):
    _id = fields.Str(dump_only=True)
    student_id = fields.Int(required=True)
    name = fields.Str(required=True)
    year = fields.Int(required=True)

class ClubSchema(Schema):
    _id = fields.Str(dump_only=True)
    club_id = fields.Int(required=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    member_count = fields.Int(dump_only=True)
