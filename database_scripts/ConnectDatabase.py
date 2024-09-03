import mysql.connector


class ConnectDatabase:

    def __init__(self,
                 user: str,
                 password: str,
                 database: str,
                 host='127.0.0.1',
                 port=3306):

        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    def __enter__(self):

        self.connection = mysql.connector.connect(user=self.user,
                                                  password=self.password,
                                                  host=self.host,
                                                  port=self.port,
                                                  database=self.database)

        self.cursor = self.connection.cursor(buffered=True)

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.connection.commit()

        self.cursor.close()

        self.connection.close()

        return False
