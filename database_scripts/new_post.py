def new_post() -> str:

    query = '''

        INSERT INTO posts VALUES(NULL, ?, ?, ?)

    '''

    return query
