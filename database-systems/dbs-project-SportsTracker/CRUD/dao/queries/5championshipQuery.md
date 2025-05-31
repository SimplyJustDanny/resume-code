updateChampionship:
    query = """
        UPDATE championships
        SET name = %s, winner_team = %s, winner_year = %s
        WHERE id = %s
        RETURNING id, name, winner_team, winner_year;
    """
    cur.execute(query, (updated_name, updated_winner_team, updated_winner_year, championship_id))
    championship = cur.fetchone()


getAllChampionships:
    query = """
        SELECT id, name, winner_team, winner_year
        FROM championships;
    """
    cur.execute(query)
    championships = cur.fetchall()


getChampionshipById:
    query = """
        SELECT c.id, c.name, c.winner_team, c.winner_year,
            t.id AS team_id, t.name AS team_name
        FROM championships c
        JOIN teams t ON c.winner_team = t.id
        WHERE c.id = %s;
    """
    cur.execute(query, (championship_id,))
    championship = cur.fetchone()


deleteChampionship:
    query = """
        DELETE FROM championships
        WHERE id = %s;
    """
    cur.execute(query, (championship_id,))


addSportToExercise:
    query = """
        INSERT INTO sport_exercises (sport, exercise)
        VALUES (%s, %s)
        RETURNING sport, exercise;
    """
    cur.execute(query, (sport_id, exercise_id))
    association = cur.fetchone()


removeSportFromExercise:
    query = """
        DELETE FROM sport_exercises
        WHERE sport = %s AND exercise = %s;
    """
    cur.execute(query, (sport_id, exercise_id))
