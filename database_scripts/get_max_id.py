def get_max_id():

    query = '''
    
        SELECT MAX(id) as max_id FROM posts;
    
    '''

    return query
