
createExercise:
  query = """
  INSERT INTO exercises (name, category, equipment, mechanic, force, level, alter_id)
  VALUES (%s, %s, %s, %s, %s, %s, %s)
  RETURNING id, name, category, equipment, mechanic, force, level, alter_id;
  """
  cur.execute(query, (name, category, equipment, mechanic, force, level, alter_id))


getAllExersises
  query = """
  SELECT id, name, category, equipment, mechanic, force, level, alter_id
  FROM exercises;
  """
  cur.execute(query)


getExerciseById:
need for multiple queries and aggregate them on backend code. Supposedly, it's simpler and safer because there will be no duplicates:

  get exercise:
    query = """
    SELECT id, name, category, equipment, mechanic, force, level, alter_id
    FROM exercises
    WHERE id = %s;
    """
    cur.execute(query, (exercise_id,))

  get instructions:
    query = """
    SELECT id AS instruction_id, instruction_number, instruction AS description
    FROM exercise_instructions
    WHERE exercise_id = %s
    ORDER BY instruction_number;
    """
    cur.execute(query, (exercise_id,))

  get image paths:
    query = """
    SELECT id AS image_id, image_path AS path
    FROM exercise_images
    WHERE exercise_id = %s;
    """
    cur.execute(query, (exercise_id,))

  get primary muscles:
    query = """
    SELECT id AS muscle_id, muscle AS name
    FROM exercise_primary_muscles
    WHERE exercise_id = %s;
    """
    cur.execute(query, (exercise_id,))

  get secondary muscles:
    query = """
    SELECT id AS muscle_id, muscle AS name
    FROM exercise_secondary_muscles
    WHERE exercise_id = %s;
    """
    cur.execute(query, (exercise_id,))


updateExercise:
  query = """
  UPDATE exercises
  SET name = %s, category = %s, equipment = %s, mechanic = %s, force = %s, level = %s, alter_id = %s
  WHERE id = %s
  RETURNING id, name, category, equipment, mechanic, force, level, alter_id;
  """
  cur.execute(query, (name, category, equipment, mechanic, force, level, alter_id, exercise_id))


deleteExercise:
  query = """
  DELETE FROM exercises
  WHERE id = %s;
  """
  cur.execute(query, (exercise_id,))
