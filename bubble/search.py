#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    search
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    与Elasticsearch索引交互的实现
    
    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-05-06 15:28
 
"""

from flask import current_app as app


def add_to_index(index, model):
    if not app.es:
        return
    if not model.__searchable__:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    app.es.index(index=index, doc_type=index, id=model.id,
                 body=payload)


def remove_from_index(index, model):
    if not app.es:
        return
    if not model.__searchable__:
        return
    app.es.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page):
    if not app.es:
        return [], 0
    search = app.es.search(
        index=index, doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [hit['_id'] for hit in search['hits']['hits']]
    return ids, search['hits']['total']
