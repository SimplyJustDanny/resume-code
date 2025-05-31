from config.pgconfig import pg_config
import psycopg2

class ExercisesDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)

    def getAllExercises(self):
        cur = self.conn.cursor()
        query = "select id, alter_id, name, force, level, mechanic, equipment, category from exercises;"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result

    def insertExercise(self, name, alter_id, force, level, mechanic, equipment, category):
        cur = self.conn.cursor()
        query = "insert into exercises (name, alter_id, force, level, mechanic, equipment, category) values(%s, %s, %s, %s, %s, %s, %s) returning id"
        cur.execute(query, (name, alter_id, force, level, mechanic, equipment, category))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def getExerciseById(self, id):
        cur = self.conn.cursor()

        query1 = """
        SELECT id, name, category, equipment, mechanic, force, level, alter_id
        FROM exercises
        WHERE id = %s;
        """
        query2 = """
        SELECT id AS instruction_id, instruction_number, instruction AS description
        FROM exercise_instructions
        WHERE exercise_id = %s
        ORDER BY instruction_number;
        """
        query3 = """
        SELECT id AS image_id, image_path AS path
        FROM exercise_images
        WHERE exercise_id = %s;
        """
        query4 = """
        SELECT id AS muscle_id, muscle AS name
        FROM exercise_primary_muscles
        WHERE exercise_id = %s;
        """
        query5 = """
        SELECT id AS muscle_id, muscle AS name
        FROM exercise_secondary_muscles
        WHERE exercise_id = %s;
        """

        result = []
        cur.execute(query1, (id,))
        result.append(cur.fetchall())
        cur.execute(query2, (id,))
        result.append(cur.fetchall())
        cur.execute(query3, (id,))
        result.append(cur.fetchall())
        cur.execute(query4, (id,))
        result.append(cur.fetchall())
        cur.execute(query5, (id,))
        result.append(cur.fetchall())
        cur.close()
        return result
    
    def updateExercise(self, id, name, alter_id, force, level, mechanic, equipment, category):
        cur = self.conn.cursor()
        query = "update exercises set name = %s, alter_id = %s, force = %s, level = %s, mechanic = %s, equipment = %s, category = %s where id = %s returning id"
        cur.execute(query, (name, alter_id, force, level, mechanic, equipment, category, id))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def deleteExercise(self, id):
        cur = self.conn.cursor()
        query = """
        DELETE FROM exercises AS e
        WHERE e.id = %s
        AND NOT EXISTS (
            SELECT 1 FROM exercise_instructions AS ei
            WHERE e.id = ei.exercise_id
        )
        AND NOT EXISTS (
            SELECT 1 FROM exercise_primary_muscles AS epm
            WHERE e.id = epm.exercise_id
        )
        AND NOT EXISTS (
            SELECT 1 FROM exercise_secondary_muscles AS esm
            WHERE e.id = esm.exercise_id
        )
        AND NOT EXISTS (
            SELECT 1 FROM exercise_images AS eimg
            WHERE e.id = eimg.exercise_id
        )
        AND NOT EXISTS (
            SELECT 1 FROM sport_exercises AS se
            WHERE e.id = se.exercise
        )
        """
        cur.execute(query, (id,))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result
        
    def getTopFiveExercises(self):
        cur = self.conn.cursor()
        query = """
        SELECT e.id AS exercise_id, e.name, COUNT(s.id) AS sports_related
        FROM sport_exercises
        JOIN exercises AS e ON exercise = e.id
	    JOIN sports AS s ON sport = s.id
	    GROUP BY exercise_id
        ORDER BY sports_related DESC
        LIMIT 5;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result

    def getExercisesByMuscle(self, muscle):
        cur = self.conn.cursor()
        query = """
        SELECT DISTINCT e.id AS exercise_id, e.name
        FROM exercises AS e
        JOIN exercise_primary_muscles AS pm ON e.id = pm.exercise_id
        JOIN exercise_secondary_muscles AS sm ON e.id = sm.exercise_id
        WHERE pm.muscle = %s OR sm.muscle = %s;
        """
        cur.execute(query, (muscle, muscle,))
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
        
    def getMostComplexExercises(self):
        cur = self.conn.cursor()
        query = """
        WITH muscles AS (
            SELECT exercise_id, muscle FROM exercise_primary_muscles
            UNION
            SELECT exercise_id, muscle FROM exercise_secondary_muscles
        ),
        muscle_groups AS (
            SELECT exercise_id, ARRAY_AGG(DISTINCT muscle) AS muscles, COUNT(DISTINCT muscle) AS muscle_count
            FROM muscles
            GROUP BY exercise_id
        ),
        ranked_exercises AS (
            SELECT e.id, e.name, mg.muscles, RANK() OVER (ORDER BY mg.muscle_count DESC) AS most_muscles_rank
            FROM exercises AS e
            JOIN muscle_groups AS mg ON e.id = mg.exercise_id
        )
        SELECT id AS exercise_id, name, muscles
        FROM ranked_exercises
        WHERE most_muscles_rank = 1;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        cur.close()
        return result
