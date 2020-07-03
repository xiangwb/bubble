from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from bubble.extensions import apispec
from bubble.api.resource import SubjectCategoryListResource, SubjectCategoryResource
from bubble.api.schema import SubjectCategorySchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(SubjectCategoryResource, "/subject-category/<string:_id>")
api.add_resource(SubjectCategoryListResource, "/users/")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=SubjectCategorySchema)
    apispec.spec.path(view=SubjectCategoryResource, app=current_app)
    apispec.spec.path(view=SubjectCategoryListResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
