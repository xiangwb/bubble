from bubble.extensions import pwd_context
from bubble.models.mongo import CommonDocument, SearchableMixin
import mongoengine as mg


class User(CommonDocument, SearchableMixin):
    """Basic user model
    """

    username = mg.StringField(required=True, max_length=100, unique=True)
    email = mg.StringField(required=False, max_length=80)
    password = mg.StringField(required=True, max_length=255)
    active = mg.BooleanField(default=True)
    __searchable__ = ['username', 'email']  # 定义需要es搜索的字段，不定义则不需要es搜索功能

    def clean(self, **kwargs):
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username
