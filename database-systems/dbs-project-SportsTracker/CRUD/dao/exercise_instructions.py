
from config.pgconfig import pg_config
import psycopg2

class ExerciseInstructionsDAO():
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user=%s" % \
        (pg_config['database'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user'])
        self.conn = psycopg2.connect(url)
    
    def insertExerciseInstruction(self, exercise_id, instruction_number, instruction):
        cur = self.conn.cursor()
        query = "insert into exercise_instructions (exercise_id, instruction_number, instruction) values(%s, %s, %s) returning id"
        cur.execute(query, (exercise_id, instruction_number, instruction))
        result = cur.fetchone()[0]
        self.conn.commit()
        cur.close()
        return result
    
    def deleteExerciseInstructions(self, exercise_id, instruction_id):
        cur = self.conn.cursor()
        query = "delete from exercise_instructions where exercise_id = %s AND exercise_instructions.id = %s"
        cur.execute(query, (exercise_id, instruction_id))
        result = cur.rowcount
        self.conn.commit()
        cur.close()
        return result


