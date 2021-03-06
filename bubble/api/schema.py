import traceback

from bubble.extensions import ma
from .adapter import get_user
from bubble.extensions import logger


class SubjectCategorySchema(ma.Schema):
    id = ma.String(dump_only=True)
    name = ma.String(required=True)
    parent = ma.String(required=False)
    path = ma.String(required=False, dump_only=True)


class SubjectSchema(ma.Schema):
    id = ma.String(dump_only=True)
    creator = ma.Method('get_creator', dump_only=True)
    category = ma.List(ma.String, load_only=True)
    category_show = ma.List(ma.String, dump_only=True)
    name = ma.String(required=True)
    desc = ma.String(required=True)

    def get_creator(self, obj):
        try:
            creator_id = obj.creator_id
            user = get_user(creator_id)
            return user
        except Exception:
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())


class ItemSchema(ma.Schema):
    id = ma.String(dump_only=True)
    question = ma.String(required=True)
    answer = ma.String(required=True)
    refer = ma.String(required=False, default='')
    point = ma.List(ma.String, load_only=True)
    point_show = ma.List(ma.String, dump_only=True)
    subject = ma.String(load_only=True)
    subject_show = ma.String(dump_only=True)


class PointSchema(ma.Schema):
    subject_id = ma.String(load_only=True,required=True)
    name = ma.String(required=True)


class PointRelationSchema(ma.Schema):
    subject_id = ma.String(required=True)
    graph = ma.Dict(required=True)