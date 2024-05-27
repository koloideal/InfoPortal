def sql_create_database() -> str:

    sql_create_db = '''
    
        CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          title TEXT,
                                          content TEXT,
                                          time INTEGER)
    
    '''

    return sql_create_db


def sql_get_post_database() -> str:

    sql_get_post = '''
    
        SELECT * FROM posts WHERE id = ?
    
    '''

    return sql_get_post


def sql_get_posts_database() -> str:

    sql_get_posts = '''

        SELECT * FROM posts ORDER BY time DESC 

    '''

    return sql_get_posts


def sql_new_post_database() -> str:

    sql_new_post = '''
    
    INSERT INTO posts VALUES(NULL, ?, ?, ?)
    
    '''

    return sql_new_post
