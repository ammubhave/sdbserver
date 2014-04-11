from auth.constants import PUBLIC_ACCESS_TOKEN
from auth.models import AccessToken
from django.shortcuts import get_object_or_404


COMMON_PRIVILEGES = [('Directory.id', 'R', ('=', 'id', 1)),
                     ('Directory.username', 'R', ()),
                     ('Directory.firstname', 'R', ()),
                     ('Directory.lastname', 'R', ()), ]


def get_privileges_from_access_token(access_token):
    from datetime import datetime
    return get_object_or_404(AccessToken, access_token=access_token, expires__gt=datetime.now()).privileges


def access_token_to_privileges(access_token):
    if access_token == PUBLIC_ACCESS_TOKEN:
        return COMMON_PRIVILEGES
    return get_privileges_from_access_token(access_token)


def access_token_generator():
    import string
    import random
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))
