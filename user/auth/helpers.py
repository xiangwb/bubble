"""Various helpers for auth. Mainly about tokens blacklisting

heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/database_blacklist/blacklist_helpers.py
"""
from datetime import datetime

from flask_jwt_extended import decode_token
import mongoengine as mg

from user.models import TokenBlacklist


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.

    :param identity_claim: configured key to get user identity
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user_identity = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token["exp"])
    revoked = False

    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_id=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db_token.save()


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token["jti"]
    try:
        token = TokenBlacklist.objects.get(jti=jti)
        return token.revoked
    except (mg.DoesNotExist, mg.MultipleObjectsReturned):
        return True


def revoke_token(token_jti, user):
    """Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    """
    try:
        token = TokenBlacklist.objects.get(jti=token_jti, user_id=user)
        token.revoked = True
        token.save()
    except (mg.DoesNotExist, mg.MultipleObjectsReturned):
        raise Exception("Could not find the token {}".format(token_jti))
