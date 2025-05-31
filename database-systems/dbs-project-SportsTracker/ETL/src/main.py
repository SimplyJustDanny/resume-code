from extract import extract
from transform import transform
from load import load
from DB import DB

db = DB()
create_tables = open("create_tables.sql")
for line in create_tables:
    line = line.strip()
    if len(line) != 0:
        db.query(line)
        db.close_cursors()



# Extract
extracted_data = extract()

for table in extracted_data.items():
    print(table)



# Transform
extracted_data = transform(extracted_data)

db.query("select count(*) from sport_exercises");
# Load only if empty.
one = db.cursor.fetchone()[0]
print(one)
if one == 0:
    load(db, extracted_data)
db.close_cursors()



# Verify Results
db.query("select * from championships;")
for row in db.cursor:
    print(row)

db.close_cursors()
db.connection.close()

