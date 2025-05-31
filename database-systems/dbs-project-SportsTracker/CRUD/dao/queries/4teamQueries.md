createTeam:
    query = """
        INSERT INTO teams (name, sport)
        VALUES (%s, %s) 
        RETURNING id, name, sport;
    """
    cur.execute(query, (team_name, sport_id))
    team = cur.fetchone()

getAllTeams:
    query = """
        SELECT id, name, sport
        FROM teams;
    """
    cur.execute(query)
    teams = cur.fetchall()

getTeamById:
    query = """
        SELECT id, name, sport
        FROM teams
        WHERE id = %s;
    """
    cur.execute(query, (team_id,))
    team = cur.fetchone()

updateTeam:
    query = """
        UPDATE teams
        SET name = %s, sport = %s
        WHERE id = %s
        RETURNING id, name, sport;
    """
    cur.execute(query, (updated_name, updated_sport_id, team_id))
    team = cur.fetchone()

deleteTeam:
    query = """
        DELETE FROM teams
        WHERE id = %s;
    """
    cur.execute(query, (team_id,))
