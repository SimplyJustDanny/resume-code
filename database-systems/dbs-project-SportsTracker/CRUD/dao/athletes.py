
from config.pgconfig import pg_config
import psycopg2

class AthletesDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        # no olvidar colocar el self
        self.conn = psycopg2.connect(url)

    def IsAtheleteInDB(self, name, age, gender, height, weight):
        cur = self.conn.cursor()
        query = "select count(*) from athletes where name = %s AND age = %s AND gender = %s AND height = %s AND weight = %s;"
        cur.execute(query, (name, age, gender, height, weight))
        result = cur.fetchone()[0]
        cur.close()
        print("RESULT ATHL CHECK", result)
        return result

    def getAllAthletes(self):
        cur = self.conn.cursor()
        query = "select id, name, age, gender, height, weight from athletes;"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
    
    def getAthleteById(self, id):
        cur = self.conn.cursor()
        query = "select id, name, age, gender, height, weight from athletes where id = %s;"
        cur.execute(query, (id,))
        result = cur.fetchone()
        cur.close()
        return result
    
    def insertAthlete(self, name, age, gender, height, weight):
        cur = self.conn.cursor()
        query = "insert into athletes (name, age, gender, height, weight) values(%s, %s, %s, %s, %s) returning id"
        cur.execute(query, (name, age, gender, height, weight))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def updateAthlete(self, id, name, age, gender, height, weight):
        cur = self.conn.cursor()
        query = "update athletes set name = %s, age = %s, gender = %s, height = %s, weight = %s where id = %s returning id"
        cur.execute(query, (name, age, gender, height, weight, id,))
        result = cur.fetchone()
        self.conn.commit()
        cur.close()
        return result
    
    def deleteAthlete(self, id):
        cur = self.conn.cursor()
        query = """
        DELETE FROM athletes AS a
        WHERE a.id = %s
        AND NOT EXISTS (
            SELECT 1 FROM practices AS p
            WHERE a.id = p.fk_athlete
        )
        """
        cur.execute(query, (id,))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result


