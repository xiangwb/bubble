from bubble.extensions import ma
from bubble.models import SubjectCategory, Subject, Tag, Item


class SubjectCategorySchema(ma.Schema):
    id = ma.String(dump_only=True)
    name = ma.String(required=True)
    parent = ma.String(required=False)
    path = ma.String(required=False, dump_only=True)


class SubjectSchema(ma.Schema):
    id = ma.String(dump_only=True)
    creator_id = ma.Dict(required=True)
    category = ma.List(ma.String, load_only=True)
    category_show = ma.List(ma.String, dump_only=True)
    name = ma.String(required=True)
    desc = ma.String(required=True)
