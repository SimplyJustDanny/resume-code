
insertSport: (create) 
query = "INSERT INTO sports (name, gender, venue)
VALUES (%s, %s, %s);"
cur.execute(query, (name, gender, venue))


getAllSports
query = "SELECT  s.id, s.name AS sport_name, s.gender, s.venue, e.name AS exercise_name
FROM sports AS s
JOIN sport_exercises AS se ON s.id = se.sport
JOIN exercises AS e ON e.id = se.exercise;"
cur.execute(query)


getSportById
query = "SELECT  s.id, s.name AS sport_name, s.gender, s.venue, e.name AS exercise_name
FROM sports AS s
JOIN sport_exercises AS se ON s.id = se.sport
JOIN exercises AS e ON e.id = se.exercise
WHERE s.id = %s;"
cur.execute(query, (id))



updateSport:
query = "UPDATE sports
SET name = %s, gender = %s, venue = %s
WHERE id = %s;"
cur.execute(query, (name, gender, venue, id))


deleteSport:
query = "DELETE FROM sports
WHERE id = %s;"
cur.execute(query, (id))