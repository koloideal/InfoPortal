def create_table() -> str:

    query = '''

        CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          title TEXT,
                                          content TEXT,
                                          time INTEGER)

    '''

    return query
