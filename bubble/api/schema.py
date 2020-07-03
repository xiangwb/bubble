from bubble.extensions import ma
from bubble.models import SubjectCategory, Subject, Tag, Item


class SubjectCategorySchema(ma.Schema):
    id = ma.String(dump_only=True)
    name = ma.String(required=True)
    parent = ma.String(required=False)
    path = ma.String(required=False, dump_only=True)


