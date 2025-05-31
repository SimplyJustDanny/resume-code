
from config.pgconfig import pg_config
import psycopg2

class PrimaryMuscleDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)
    
    def insertPrimaryMuscle(self, muscle_id, muscle_description):
        cur = self.conn.cursor()
        query = "insert into exercise_primary_muscles (exercise_id, muscle) values(%s, %s) returning id"
        cur.execute(query, (muscle_id, muscle_description))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def deletePrimaryMuscle(self, exercise_id, muscle_id):
        cur = self.conn.cursor()
        query = "delete from exercise_primary_muscles where exercise_id = %s AND id = %s"
        cur.execute(query, (exercise_id, muscle_id))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result


