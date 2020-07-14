import marshmallow
import pysnooper
from flask import request
from flask_restful import Resource
import mongoengine as mg

from bubble.commons.pagination import Pagination
from bubble.extensions import logger
from bubble.models import SubjectCategory, Subject, Tag, Item
from bubble.api.schema import SubjectCategorySchema, SubjectSchema
from bubble.utils.response import format_response


class SubjectCategoryResource(Resource):
    """
    课程分类查改删
    """

    def get(self, _id):
        schema = SubjectCategorySchema()
        try:
            subject_category = SubjectCategory.objects.get(id=_id)
            return format_response(schema.dump(subject_category), "get subject category detail success", 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'subject category is not exist', 404)

    def put(self, _id):
        schema = SubjectCategorySchema()
        try:
            subject_category = SubjectCategory.objects.get(id=_id)
            data = schema.load(request.json)
            subject_category.update(**data)
            subject_category.reload()
            return format_response(schema.dump(subject_category), 'subject category updated', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'subject category is not exist', 404)

    def delete(self, _id):
        try:
            SubjectCategory.objects.get(id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'subject category deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'subject category is not exist', 404)


class SubjectCategoryListResource(Resource):
    """
    课程分类创建与列表
    """

    def get(self):
        try:
            schema = SubjectCategorySchema(many=True)
            subject_category_list = SubjectCategory.objects.all()
            objs, page = Pagination(subject_category_list).paginate(schema)
            return format_response(objs, 'get subject category list success', 200, page=page)
        except Exception as e:
            return format_response(e.args, 'get subject category list failure', 500)

    def post(self):
        try:
            schema = SubjectCategorySchema()
            data = schema.load(request.json)
            user = SubjectCategory.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            return format_response(schema.dump(user), 'subject category created', 201)
        except mg.errors.NotUniqueError:
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response('', 'subject category exists', 400)
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500)


class CategorySubjectResource(Resource):
    """
    查询某个课程分类下的课程
    """

    def get(self, _id):
        try:
            schema = SubjectSchema()
            subject_list = Subject.objects.get(category__id=[_id])
            objs, page = Pagination(subject_list).paginate(schema)
            return format_response(objs, 'get subject list success', 200, page=page), 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            return format_response(e.args, 'get subject list failure', 500), 500


class SubjectResource(Resource):
    """
    课程查改删接口
    """

    def get(self, _id):
        schema = SubjectSchema()
        try:
            subject = Subject.objects.get(id=_id)
            subject.category_show = [category.name for category in subject.category]
            return format_response(schema.dump(subject), "get subject detail success", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'subject is not exist', 404), 404

    def put(self, _id):
        schema = SubjectSchema()
        try:
            subject = Subject.objects.get(id=_id)
            data = schema.load(request.json)
            subject.update(**data)
            subject.reload()
            subject.category_show = [category.name for category in subject.category]
            return format_response(schema.dump(subject), "subject updated", 200), 200
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            return format_response('', 'subject is not exist', 404), 404

    def delete(self, _id):
        try:
            Subject.objects.get(id=_id).delete()
            # return {"msg": "user deleted"}
            return format_response('', 'subject  deleted', 200)
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            # abort(404, {'msg': '用户不存在'})
            return format_response('', 'subject is not exist', 404)


class SubjectListResource(Resource):
    """
    课程列表和创建
    """

    def get(self):
        try:
            schema = SubjectSchema(many=True)
            subject_list = Subject.objects.all()
            objs, page = Pagination(subject_list).paginate(schema)
            return format_response(objs, 'get subject list success', 200, page=page), 200
        except Exception as e:
            return format_response(e.args, 'get subject list failure', 500), 500

    @pysnooper.snoop()
    def post(self):
        try:
            schema = SubjectSchema()
            headers = request.headers
            logger.api_logger.info(headers)
            data = schema.load(request.json)
            creator_id = headers.get('X-Auth-User-Id')
            if not creator_id:
                return format_response("no response header X-Auth-User-Id", 'server error', 500), 500
            data['creator_id'] = creator_id
            subject = Subject.objects.create(**data)
            # return {"msg": "user created", "user": schema.dump(user)}, 201
            subject.category_show = [category.name for category in subject.category]
            return format_response(schema.dump(subject), 'subject  created', 201), 201
        except marshmallow.exceptions.ValidationError as e:
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'param error', 400), 400
        except mg.errors.NotUniqueError as e:
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            # abort(403, {'msg': '手机号码已存在'})
            return format_response(e.args, 'subject exists', 400), 400
        except Exception as e:
            # abort(500, {"msg": e.args})
            import traceback
            traceback.print_exc()
            logger.api_logger.error(traceback.format_exc())
            return format_response(e.args, 'server error', 500), 500
