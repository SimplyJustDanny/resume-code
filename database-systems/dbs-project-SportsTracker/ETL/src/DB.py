import os
import psycopg2


class DB:
    def __init__(self):
        pg_config = {
                "host": "localhost",
                "user": "postgres",
                "password": "",
                "dbname": "postgres",
                "port": 8999
        }
        # pg_config = {
        #     # REDACTED
        # }
        # conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"
        conn_string = "host=%s dbname=%s user=%s password=%s port=%s" % \
                (
                    pg_config["host"],
                    pg_config["dbname"],
                    pg_config["user"],
                    pg_config["password"],
                    pg_config["port"],
                )
        print(conn_string)
        self.connection = psycopg2.connect(conn_string)
        self.cursors = []
        self.cursor = None
        
    def query(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.connection.commit()
        self.cursors.append(self.cursor)
        return self.cursor

    def close_cursors(self):
        for cursor in self.cursors:
            cursor.close()
        self.cursors = []

