def new_post() -> str:

    query = '''

        INSERT INTO posts VALUES(%s, %s, %s, %s)

    '''

    return query
