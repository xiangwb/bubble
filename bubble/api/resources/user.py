from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required

import mongoengine as mg
from bubble.models import User
from bubble.extensions import ma
from bubble.commons.pagination import Pagination


class UserSchema(ma.Schema):
    id = ma.String(dump_only=True)
    password = ma.String(load_only=True, required=True)
    username = ma.String(required=True)


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: username
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required]

    def get(self, username):
        schema = UserSchema()
        try:
            user = User.objects.get(username=username)
            return {"user": schema.dump(user)}
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            abort(404, {'msg': '用户不存在'})

    def put(self, username):
        schema = UserSchema(partial=True)
        try:
            user = User.objects.get(username=username)
            user_data = schema.load(request.json)
            user.update(**user_data)
            user.reload()
            return {"msg": "user updated", "user": schema.dump(user)}
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            abort(404, {'msg': '用户不存在'})

    def delete(self, username):
        try:
            User.objects.get(username=username).delete()
            return {"msg": "user deleted"}
        except (mg.DoesNotExist, mg.MultipleObjectsReturned):
            abort(404, {'msg': '用户不存在'})


class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.objects.all()
        objs, page = Pagination(query).paginate(schema)
        return {'response': objs, 'page': page}

    def post(self):
        schema = UserSchema()
        data = schema.load(request.json)
        user = User.objects.create(**data)
        return {"msg": "user created", "user": schema.dump(user)}, 201
