#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    error_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    统一定义全局性的请求处理

    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-04-29 15:08

"""
import traceback

from bubble.extensions import logger
from bubble.utils.response import format_response


def register_error_handler(app):
    app.register_error_handler(400, handle_400)
    app.register_error_handler(401, handle_401)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(405, handle_405)
    app.register_error_handler(429, handle_429)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(Exception, handle_exception)


def handle_400(e):
    """捕获abort(400)错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'msg': 'Bad Request',
    #     'err': 10
    # }
    # if isinstance(e.description, int):
    #     rsp['err'] = e.description
    # if isinstance(e.description, dict):
    #     rsp.update(e.description)
    # # return jsonify(**rsp), 400
    return format_response(str(e), 'bad request', 400), 400


def handle_401(e):
    """捕获abort(401)错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'msg': 'Unauthorized',
    #     'err': 20
    # }
    # if isinstance(e.description, int):
    #     rsp['err'] = e.description
    # elif isinstance(e.description, dict):
    #     rsp.update(e.description)
    # return jsonify(**rsp), 401
    return format_response(str(e), 'Unauthorized', 401), 401


def handle_403(e):
    """捕获abort(403)错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'err': 400,
    #     'msg': 'Forbidden'
    # }
    # if isinstance(e.description, int):
    #     rsp['err'] = e.description
    # if isinstance(e.description, dict):
    #     rsp.update(e.description)
    # return jsonify(**rsp), 403
    return format_response(str(e), 'Forbidden', 403), 403


def handle_404(e):
    """捕获abort(404)错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'msg': 'Not Found',
    #     'err': 50
    # }
    # if isinstance(e.description, dict):
    #     rsp.update(e.description)
    # return jsonify(**rsp), 404
    logger.info("url not found")
    return format_response(str(e), 'Not Found', 404), 404


def handle_405(e):
    """捕获abort(405)错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'msg': 'Method not allowed',
    #     'err': 60
    # }
    # return jsonify(**rsp), 405
    return format_response(str(e), 'Method not allowed', 405), 405


def handle_429(e):
    """捕获abort(429)频率限制错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'msg': 'Too Many Requests',
    #     'err': 30
    # }
    # err_info = {
    #     'msg': 'Too many requests',
    #     'ip': request.remote_addr,
    #     'url': request.url,
    #     'method': request.method,
    # }
    # logger.api_logger.error(err_info)
    # return jsonify(**rsp), 429
    return format_response(str(e), 'Too many requests', 429), 429


def handle_500(e):
    """捕获500错误"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # rsp = {
    #     'msg': 'Too Many Requests',
    #     'err': 30
    # }
    # err_info = {
    #     'msg': 'Too many requests',
    #     'ip': request.remote_addr,
    #     'url': request.url,
    #     'method': request.method,
    # }
    # logger.api_logger.error(err_info)
    # return jsonify(**rsp), 429
    return format_response(str(e), 'server error', 500), 500


def handle_exception(e):
    """Called when exception occurred"""
    traceback.print_exc()
    logger.api_logger.error(traceback.format_exc())
    # return jsonify(str(e)), 500
    return format_response(str(e), 'server error', 500), 500
