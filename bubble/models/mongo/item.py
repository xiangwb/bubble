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
    问题知识点
    """
    name = mg.StringField(required=True, max_length=100, unique=True)

    def __repr__(self):
        return "<Point %s>" % self.name

    def __str__(self):
        return "{}".format(self.name)


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

    # __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    def __repr__(self):
        return "<Item %s>" % self.id


class PointRelation(CommonDocument):
    """
    知识点图谱三元组
    """
    subject = mg.ReferenceField(Subject, reverse_delete_rule=mg.CASCADE)
    p1 = mg.ReferenceField(Point, reverse_delete_rule=mg.CASCADE)
    relation = mg.StringField(required=True)
    p2 = mg.ReferenceField(Point, reverse_delete_rule=mg.CASCADE, required=False)
    sequence = mg.IntField(min_value=1)  # 标识序号

    def __repr__(self):
        return "<PointRelation {}_{}_{}_{}>".format(self.subject.name, self.p1.name, self.relation,
                                                    self.p2.name if self.p2 else "None")
