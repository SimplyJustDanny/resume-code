from config.pgconfig import pg_config
import psycopg2

url = "dbname = %s password=%s host=%s port=%s user=%s" % \
(pg_config['database'],
pg_config['password'],
pg_config['host'],
pg_config['port'],
pg_config['user'])

conn = psycopg2.connect(url)

tables_to_alter = [
    "sports",
    "exercises",
    "exercise_instructions",
    "exercise_primary_muscles",
    "exercise_secondary_muscles",
    "exercise_images",
    "teams",
    "championships",
    "athletes"
]
cur = conn.cursor()

for table in tables_to_alter:
    query = "select max(id) + 1 from " + table + ";"
    print(query)
    cur.execute(query)
    new_id = cur.fetchone()[0]
    query = "alter sequence " + table + "_id_seq restart with " + str(new_id)
    print(query)
    print()
    cur.execute(query)

conn.commit()
cur.close()
conn.close()

