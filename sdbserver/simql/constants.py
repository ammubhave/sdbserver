from simql.models import Directory


TABLES = {
    'directory': Directory
}

ALLOWED_COLUMNS = {
    Directory: ['username', 'firstname', 'lastname', 'cellphone', 'email', 'phone', 'year', 'id', 'room', 'homepage', 'home_city', 'home_state', 'home_country', 'quote']
}


OP_TO_COLUMN_SUFFIX = {
    '=': '',
    '>': '__gt',
    '>=': '__gte',
    '<': '__lt',
    '<=': '__lte',
    '!=': '~',
    '<>': '~',
}