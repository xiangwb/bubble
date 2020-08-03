from bubble.extensions import ma
from bubble.models import SubjectCategory, Subject, Point, Item


class SubjectCategorySchema(ma.Schema):
    id = ma.String(dump_only=True)
    name = ma.String(required=True)
    parent = ma.String(required=False)
    path = ma.String(required=False, dump_only=True)


class SubjectSchema(ma.Schema):
    id = ma.String(dump_only=True)
    creator_id = ma.String(dump_only=True)
    category = ma.List(ma.String, load_only=True)
    category_show = ma.List(ma.String, dump_only=True)
    name = ma.String(required=True)
    desc = ma.String(required=True)


class ItemSchema(ma.Schema):
    id = ma.String(dump_only=True)
    question = ma.String(required=True)
    answer = ma.String(required=True)
    refer = ma.String(required=False, default='')
    point = ma.List(ma.String, load_only=True)
    poing_show = ma.List(ma.String, dump_only=True)
    subject = ma.String(load_only=True)
    subject_show = ma.String(dump_only=True)
