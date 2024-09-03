def get_posts() -> str:

    query = '''

        SELECT * FROM posts ORDER BY time DESC 

    '''

    return query
