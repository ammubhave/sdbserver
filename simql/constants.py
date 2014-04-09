frim simql.models import Directory


TABLES = {
    'directory': Directory
}

ALLOWED_COLUMNS = {
    Directory: ['username', 'firstname', 'lastname', 'cellphone', 'email', 'phone', 'year', 'id', 'room']
}