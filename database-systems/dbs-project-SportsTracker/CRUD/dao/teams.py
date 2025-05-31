
from config.pgconfig import pg_config
import psycopg2

class TeamsDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)

    def IsTeamInDB(self, name, sport):
        cur = self.conn.cursor()
        query = "select count(*) from teams where name = %s and sport = %s;"
        cur.execute(query, (name, sport,))
        result = cur.fetchone()[0]
        cur.close()
        print("RESULT", result)
        return result

    def getAllTeams(self):
        cur = self.conn.cursor()
        query = "select id, name, sport from teams;"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
    
    def getTeamById(self, id):
        cur = self.conn.cursor()
        query = "select id, name, sport from teams where id = %s;"
        cur.execute(query, (id,))
        result = cur.fetchone()
        cur.close()
        return result
    
    def insertTeam(self, name, sport):
        cur = self.conn.cursor()
        query = "insert into teams (name, sport) values(%s, %s) returning id"
        cur.execute(query, (name, sport))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def updateTeamById(self, id, name, sport):
        cur = self.conn.cursor()
        query = "update teams set name = %s, sport = %s where id = %s; select id, name, sport from teams where id = %s;"
        cur.execute(query, (name, sport, id, id,))
        result = cur.fetchone()
        self.conn.commit()
        cur.close()
        return result
    
    def deleteTeam(self, id):
        cur = self.conn.cursor()
        query = """
        DELETE FROM teams AS t
        WHERE t.id = %s
        AND NOT EXISTS (
            SELECT 1 FROM championships AS c
            WHERE t.id = c.winner_team
        )
        AND NOT EXISTS (
            SELECT 1 FROM practices AS p
            WHERE t.id = p.fk_team
        )
        """
        cur.execute(query, (id,))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result
        
    def getTopThreeTeams(self):
        cur = self.conn.cursor()
        query = """
        SELECT t.id as team_id, t.name, s.name AS sport, COUNT(c.id) as championships_won
        FROM championships AS c
	    JOIN teams AS t ON c.winner_team = t.id
        JOIN sports AS s ON t.sport = s.id
	    GROUP BY team_id, s.name
        ORDER BY championships_won DESC
        LIMIT 3;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result

    def getMostTeamsPerSport(self):
        cur = self.conn.cursor()
        query = """
        SELECT s.name AS sport, COUNT(t.id) AS team_count
        FROM teams AS t
	    JOIN sports AS s ON t.sport = s.id
	    GROUP BY s.name
	    ORDER BY team_count DESC;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result

