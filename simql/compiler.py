from constants import ALLOWED_COLUMNS, TABLES


def compile_columns(table, columns):
    """Check for valid column entries and expand if necessary

    If columns is the string '*' then it is expanded into list
    of all allowed columns.

    If columns contains a not-allowed column then raises an
    Exception.

    @param table the table for which the column entries are for
    @param columns the column entries which have to be compiler
    @returns the compiled column list
    @throws Exception if any column in columns is not allowed
    """
    if columns == '*':
        return ALLOWED_COLUMNS[table]

    compiled_columns = []
    for column in columns:
        column = column.lower()
        if column in ALLOWED_COLUMNS[table]:
            compiled_columns.append(column)
        else:
            raise Exception('Invalid column ' + column)
    return compiled_columns
