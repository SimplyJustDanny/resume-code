
from config.pgconfig import pg_config
import psycopg2

class ImageDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)
    
    def insertImage(self, muscle_id, path):
        cur = self.conn.cursor()
        query = "insert into exercise_images (exercise_id, image_path) values(%s, %s) returning id"
        cur.execute(query, (muscle_id, path))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def deleteImage(self, exercise_id, path):
        cur = self.conn.cursor()
        query = "delete from exercise_images where exercise_id = %s AND id = %s"
        cur.execute(query, (exercise_id, path))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result


