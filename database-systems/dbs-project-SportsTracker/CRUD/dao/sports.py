
from config.pgconfig import pg_config
import psycopg2

class SportsDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)

    def getAllSports(self):
        cur = self.conn.cursor()
        query = "select id, name, gender, venue from sports;"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
    
    def getSportById(self, id):
        cur = self.conn.cursor()
        query = "select sports.id, sports.name, sports.gender, sports.venue, exercises.id, exercises.name from sports "
        query += "inner join sport_exercises on sports.id = sport_exercises.sport "
        query += "inner join exercises on sport_exercises.exercise = exercises.id "
        query += "where sports.id = %s"
        cur.execute(query, (id,))
        result = cur.fetchall()
        val = False
        if len(result) == 0:
            val = True
            query = "select sports.id, sports.name, sports.gender, sports.venue from sports;"
            cur.execute(query, (id,))
            result = cur.fetchall()

        cur.close()
        return (val, result)
    
    def insertSport(self, name, gender, venue):
        cur = self.conn.cursor()
        query = "insert into sports ( name, gender, venue) values(%s, %s, %s) returning id"
        cur.execute(query, (name, gender, venue))
        id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return id
    
    def updateSport(self, id, name, gender, venue):
        cur = self.conn.cursor()
        query = "update sports set name = %s, gender = %s, venue = %s where id = %s returning id"
        cur.execute(query, (name, gender, venue, id,))
        result = cur.fetchone()
        self.conn.commit()
        cur.close()
        return result
    
    def deleteSport(self, id):
        cur = self.conn.cursor()
        query = """
        DELETE FROM sports AS s
        WHERE s.id = %s
        AND NOT EXISTS (
            SELECT 1 FROM sport_exercises AS se
            WHERE s.id = se.sport
        )
        AND NOT EXISTS (
            SELECT 1 FROM teams AS t
            WHERE s.id = t.sport
        )
        """
        cur.execute(query, (id,))
        result = cur.rowcount
        print(result)
        self.conn.commit()
        cur.close()
        return result

    def addSportToExercise(self, exercise_id, sport_id):
        cur = self.conn.cursor()
        query = "insert into sport_exercises (sport, exercise) values(%s, %s) returning (sport, exercise)"
        cur.execute(query, (sport_id, exercise_id))
        result = cur.fetchone()
        self.conn.commit()
        cur.close()
        return result

    def removeSportFromExercise(self, exercise_id, sport_id):
        cur = self.conn.cursor()
        query = "delete from sport_exercises where sport = %s and exercise = %s"
        cur.execute(query, (sport_id, exercise_id))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result

    def getMostPopularSports(self):
        cur = self.conn.cursor()
        query = """
        SELECT s.name AS sport, COUNT(a.id) AS athlete_count
        FROM practices
        JOIN athletes AS a ON fk_athlete = a.id
        JOIN teams AS t ON fk_team = t.id
	    JOIN sports AS s ON s.id = t.sport
	    GROUP BY s.name
	    ORDER BY athlete_count DESC
        LIMIT 5;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
