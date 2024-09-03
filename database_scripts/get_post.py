def get_post() -> str:

    query = '''

        SELECT * FROM posts WHERE id = ?

    '''

    return query
