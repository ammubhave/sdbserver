from .constants import PUBLIC_ACCESS_TOKEN


COMMON_PRIVILEGES = [('Directory.id', 'R', ('=', 'id', 1)),
                     ('Directory.username', 'R', ()),
                     ('Directory.firstname', 'R', ()), ]


def access_token_to_privileges(access_token):
    if access_token == PUBLIC_ACCESS_TOKEN:
        return COMMON_PRIVILEGES

