from config.pgconfig import pg_config
import psycopg2

class UserDAO:
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user= %s" % \
              (pg_config['database'],
               pg_config['password'],
               pg_config['host'],
               pg_config['port'],
               pg_config['user']
               )
        self.conn = psycopg2.connect(url)

    def insertUser(self, email, username, userpassword, created):
        cursor = self.conn.cursor()
        query = "insert into users (email, username, userpassword, created) values(%s, %s, %s, %s) returning id"
        cursor.execute(query, (email, username, userpassword, created,))
        self.conn.commit()
        cursor.close()
        return

    def emailInDB(self,email):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE email = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        else:
            return False

    def nameInDB(self,username):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        else:
            return False

    def getUserByEmail(self,email):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE email = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result
        
