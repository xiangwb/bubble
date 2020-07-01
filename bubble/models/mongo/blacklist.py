"""Simple blacklist implementation using database

Using database may not be your prefered solution to handle blacklist in your
final application, but remember that's just a cookiecutter template. Feel free
to dump this code and adapt it for your needs.

For this reason, we don't include advanced tokens management in this
example (view all tokens for a user, revoke from api, etc.)

If we choose to use database to handle blacklist in this example, it's mainly
because it will allow you to run the example without needing to setup anything else
like a redis or a memcached server.

This example is heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/database_blacklist/
"""
from bubble.models.mongo import CommonDocument
import mongoengine as mg


class TokenBlacklist(CommonDocument):
    """Blacklist representation
    """

    jti = mg.StringField(required=True, max_length=36, unique=True)
    token_type = mg.StringField(required=True, max_length=10)
    user_id = mg.StringField(required=True, max_length=36)  # 相当于用户的外键
    revoked = mg.BooleanField(required=True)
    expires = mg.DateTimeField(required=True)

    def to_dict(self):
        return {
            "token_id": self.id,
            "jti": self.jti,
            "token_type": self.token_type,
            "revoked": self.revoked,
            "expires": self.expires,
            "user_id": self.user_id,
        }
