from mongoengine import signals

from bubble.models.mongo import CommonDocument
import mongoengine as mg


class SubjectCategory(CommonDocument):
    """
    课程分类模型：树形结构
    """
    name = mg.StringField(required=True, max_length=100)
    parent = mg.ReferenceField('self')
    path = mg.StringField(required=False)

    def __repr__(self):
        return "<Category %s>" % self.name

    def __str__(self):
        return "{}_{}".format(self.path, self.name)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if document.parent is None:
            document.path = '/'
        else:
            # document.path = '{}/{}'.format(document.parent.path, document.parent.name)
            parent = document.parent
            if parent.path == '/':
                document.path = parent.path + parent.name
            else:
                document.path = parent.path + '/' + parent.name

    meta = {
        'indexes': [{'fields': ['name', 'path'], 'unique': True}, ]
    }


signals.pre_save.connect(SubjectCategory.pre_save, sender=SubjectCategory)


class Subject(CommonDocument):
    """
    课程模型
    """
    name = mg.StringField(required=True, max_length=100, unique=True)
    creator_id = mg.StringField(required=True)
    category = mg.ListField(mg.ReferenceField(SubjectCategory))
    desc = mg.StringField(required=True)

    def __repr__(self):
        return "<Subject %s>" % self.name

    def __str__(self):
        return "{}".format(self.name)


class Point(CommonDocument):
    """
    课程知识点
    """
    subject_id = mg.StringField(required=True)
    name = mg.StringField(required=True, max_length=100, unique=True)

    def __repr__(self):
        return "<Point %s_%s>" % (self.subject_id, self.name)

    def __str__(self):
        return "{}".format(self.name)

    meta = {
        'indexes': [{'fields': ['subject_id', 'name'], 'unique': True}, ]
    }


class Item(CommonDocument):
    """
    问题条目
    """

    question = mg.StringField(required=True)
    answer = mg.StringField(required=False)
    refer = mg.StringField(required=True)
    point = mg.ListField(mg.ReferenceField(Point))
    subject = mg.ReferenceField(Subject, reverse_delete_rule=mg.CASCADE)
    creator_id = mg.StringField(required=True)
    sequence = mg.IntField(min_value=1, default=1)

    # __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    def __repr__(self):
        return "<Item %s>" % self.id


class PointRelation(CommonDocument):
    """
    知识点图谱三元组
    graph的数据结构
    【
        {id:1234,,contains:[{"id":1234,"contains":[{"id":"3344"}]},
        {...}
    】
    """
    subject = mg.ReferenceField(Subject, reverse_delete_rule=mg.CASCADE, unique=True)  # 关联课程
    # n1_type = mg.StringField(required=True, choices=('subject', 'point'))  # 节点1定义，节点1只能是point
    # n1_id = mg.StringField(required=True)  # 节点2id
    # relation = mg.StringField(required=True, choices=['contains', ])  # 节点间关系
    # n2_type = mg.StringField(required=True, choices=('point', 'item'))  # 节点2类型,如果节点1的类型为subject，那么节点2的类型只能是point
    # n2_id = mg.StringField(required=True)  # 节点2id
    # sequence = mg.IntField(min_value=1, default=1)  # 标识序号
    graph = mg.DictField(required=True)

    def __repr__(self):
        return "<PointRelation {}>".format(self.subject.name)


class UserSubject(CommonDocument):
    """
    用户课程情况
    detail数据结构：
    {
        "points":{
        },
        "items":{
        },
        "latest":{"item_id":"a1d323brd","answer":1}
    }
    """
    user_id = mg.StringField(required=True)  # 用户ID
    subject_id = mg.ReferenceField(Subject, reverse_delete_rule=mg.CASCADE)
    detail = mg.DictField(required=True)  # 知识点掌握情况

    def __repr__(self):
        return "<UserItem {}".format(self.user_id)
