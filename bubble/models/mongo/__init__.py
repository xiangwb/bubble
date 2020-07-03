#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    mongodb的model定义文件
    
    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-04-24 11:27
 
"""

from datetime import datetime

from bson import ObjectId
from mongoengine import QuerySet, Document, BooleanField, DateTimeField, StringField, signals
# from bubble.search import add_to_index, remove_from_index


class ValidQuerySet(QuerySet):

    def valid_objs(self, *q_objs, **kwargs):
        return self.filter(is_deleted=False, *q_objs, **kwargs)

    def exists(self, *q_objs, **kwargs):
        return bool(self.filter(is_deleted=False, *q_objs, **kwargs).first())

    def valid_get(self, *q_objs, **kwargs):
        return self.get(is_deleted=False, *q_objs, **kwargs)


class CommonDocument(Document):
    id = StringField(name='_id', primary_key=True)
    is_deleted = BooleanField(default=False)
    create_time = DateTimeField()
    update_time = DateTimeField(default=datetime.utcnow)
    __searchable__ = []

    meta = {
        'abstract': True,
        'queryset_class': ValidQuerySet
    }


def pre_save(sender, document, **kwargs):
    """ 在 save 方法执行之前执行 """
    if not document.create_time:
        document.create_time = datetime.utcnow()
        document.id = ObjectId().__str__()
    document.update_time = datetime.utcnow()


def pre_bulk_insert(sender, documents, **kwargs):
    """ 批量插入执行之前执行 """
    now = datetime.utcnow()
    for document in documents:
        if not document.create_time:
            document.create_time = now
            document.id = ObjectId().__str__()
        document.update_time = now


def post_save(sender, document, **kwargs):
    """ 在 save 方法执行之后执行 """
    # FIXME: 配合软删得做一些额外的工作
    doc_col = document.__class__.__dict__['_meta']['collection']
    # 插入数据到es
    # add_to_index(doc_col, document)


def post_delete(sender, document, **kwargs):
    """ 在 删除 方法执行之后执行 """
    doc_col = document.__class__.__dict__['_meta']['collection']
    # 删除es的数据
    # remove_from_index(doc_col, document)


def post_bulk_insert(sender, documents, **kwargs):
    """ 批量插入执行之后执行 """
    pass


# class SearchableMixin(object):
#
#     @classmethod
#     def reindex(cls):
#         for obj in cls.objects.filter(is_deleted=False):
#             add_to_index(cls.__dict__['_meta']['collection'], obj)


# 注册信号
signals.pre_save.connect(pre_save)
signals.pre_bulk_insert.connect(pre_bulk_insert)
signals.post_save.connect(post_save)
signals.post_delete.connect(post_delete)
signals.post_bulk_insert.connect(post_bulk_insert)

