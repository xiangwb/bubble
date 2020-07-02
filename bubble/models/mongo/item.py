from mongoengine import signals

from bubble.models.mongo import CommonDocument, SearchableMixin
import mongoengine as mg


class SubjectCategory(CommonDocument, SearchableMixin):
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
            document.path = '{}/{}'.format(document.parent.path, document.parent.name)


signals.pre_save.connect(SubjectCategory.pre_save, sender=SubjectCategory)


class Subject(CommonDocument, SearchableMixin):
    """
    课程模型
    """
    name = mg.StringField(required=True, max_length=100, unique=True)
    category = mg.ListField(mg.EmbeddedDocument(SubjectCategory))
    desc = mg.StringField(required=True)

    def __repr__(self):
        return "<Subject %s>" % self.name

    def __str__(self):
        return "{}".format(self.name)


class Tag(CommonDocument, SearchableMixin):
    """
    问题标签
    """
    name = mg.StringField(required=True, max_length=100, unique=True)

    def __repr__(self):
        return "<Tag %s>" % self.name

    def __str__(self):
        return "{}".format(self.name)


class Item(CommonDocument, SearchableMixin):
    """
    问题条目
    """

    question = mg.StringField(required=True)
    answer = mg.StringField(required=False)
    refer = mg.StringField(default=True)
    tag = mg.ListField(mg.EmbeddedDocument(Tag))
    subject_id = mg.ReferenceField(Subject, reverse_delete_rule=mg.CASCADE)

    # __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    def __repr__(self):
        return "<Item %s>" % self.id
