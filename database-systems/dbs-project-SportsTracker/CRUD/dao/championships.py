from config.pgconfig import pg_config
import psycopg2

class ChampionshipsDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)

    def getAllChampionships(self):
        cur = self.conn.cursor()
        query = "select id, name, winner_team, winner_year from championships;"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
    
    def getChampionshipById(self, id):
        cur = self.conn.cursor()
        query = "select id, name, winner_team, winner_year from championships where id = %s;"
        cur.execute(query, (id,))
        result = cur.fetchone()
        if result:
            query = "select id, name from teams where id = %s"
            cur.execute(query, (result[2],))
            result = (result, cur.fetchone())
            cur.close()
        return result
    
    def insertChampionship(self, name, winner_team, winner_year):
        cur = self.conn.cursor()
        query = "insert into championships (name, winner_team, winner_year) values(%s, %s, %s) returning id"
        cur.execute(query, (name, winner_team, winner_year))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def updateChampionship(self, id, name, winner_team, winner_year):
        cur = self.conn.cursor()
        query = "update championships set name = %s, winner_team = %s, winner_year = %s where id = %s returning id"
        cur.execute(query, (name, winner_team, winner_year, id,))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def deleteChampionship(self, id):
        cur = self.conn.cursor()
        query = "delete from championships where id = %s"
        cur.execute(query, (id,))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result

    def getMostWonChampionships(self):
        cur = self.conn.cursor()
        query = """
        SELECT t.id AS team_id, t.name, COUNT(c.id) as total_wins
        FROM championships AS c
	    JOIN teams AS t ON c.winner_team = t.id
	    GROUP BY t.id
	    ORDER BY total_wins DESC
        LIMIT 5;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
