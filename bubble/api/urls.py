from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from bubble.extensions import apispec
from bubble.api.resource import SubjectCategoryListResource, SubjectCategoryResource, SubjectResource, \
    SubjectListResource, CategorySubjectResource, ItemResource, ItemListResource, PointResource
from bubble.api.schema import SubjectCategorySchema

blueprint = Blueprint("api", __name__, url_prefix="/api/v1/bubble")
api = Api(blueprint)

api.add_resource(SubjectCategoryResource, "/subject-categories/<string:_id>/")
api.add_resource(SubjectCategoryListResource, "/subject-categories/")
api.add_resource(CategorySubjectResource, "/subject-categories/<string:_id>/subjects/")
api.add_resource(SubjectResource, "/subjects/<string:_id>/")
api.add_resource(SubjectListResource, "/subjects/")
api.add_resource(ItemResource, "/items/<string:_id>/")
api.add_resource(ItemListResource, "/items/")
api.add_resource(PointResource, '/points/')


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("SubjectCategorySchema", schema=SubjectCategorySchema)
    apispec.spec.path(view=SubjectCategoryResource, app=current_app)
    apispec.spec.path(view=SubjectCategoryListResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
