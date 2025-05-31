from config.pgconfig import pg_config
import psycopg2

class FragmentDAO:
    def __init__(self):
        url = "dbname = %s password=%s host=%s port=%s user= %s" % \
              (pg_config['database'],
               pg_config['password'],
               pg_config['host'],
               pg_config['port'],
               pg_config['user']
               )
        self.conn = psycopg2.connect(url)

    def insertFragment(self, content, embedding):
        cursor = self.conn.cursor()
        query = "insert into exercise_fragments(content, embedding) values (%s, %s) returning ctxid"
        cursor.execute(query, (content, embedding,))
        fid = cursor.fetchone()[0]
        self.conn.commit()
        return fid

    def getFragments(self,emb):
        cursor = self.conn.cursor()
        query = ("select ctxid, content from exercise_fragments order by embedding <-> %s, ctxid limit 3")
        cursor.execute(query, (emb,))
        result = []
        for row in cursor:
            result.append(row)
        return result
