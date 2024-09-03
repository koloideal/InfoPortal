def new_post() -> str:

    query = '''

        INSERT INTO posts VALUES(?, ?, ?, ?)

    '''

    return query
