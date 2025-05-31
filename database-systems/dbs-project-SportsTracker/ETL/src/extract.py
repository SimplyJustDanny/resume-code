import polars as pl
import sqlite3
import numpy as np

def extract():
    exercise_images = pl.read_json("../../ETL_sources/exercise_images.json")
    exercise_instructions = pl.read_json("../../ETL_sources/exercise_instructions.json")
    exercise_primary_muscles = pl.read_json("../../ETL_sources/exercise_primary_muscles.json")
    exercise_secondary_muscles = pl.read_json("../../ETL_sources/exercise_secondary_muscles.json")
    exercises = pl.read_json("../../ETL_sources/exercises.json")
    sports_with_exercises = pl.read_json("../../ETL_sources/sports_with_exercises.json")
    sports = sports_with_exercises.select([col for col in sports_with_exercises.columns if col != "exercises"])
    sport_exercises = sports_with_exercises.explode("exercises").select([pl.col("id").alias("sport"), pl.col("exercises").alias("exercise")])    
    practices = pl.read_csv("../../ETL_sources/practices.csv")
    teams = pl.read_csv("../../ETL_sources/teams_.csv")

    con = sqlite3.connect("../../ETL_sources/athletes.db")
    athletes = pl.read_database(
        query="SELECT * FROM athletes;",
        connection=con
    )
    con.close()

    con = sqlite3.connect("../../ETL_sources/championships.db")
    championships = pl.read_database(
        query="SELECT * FROM championships;",
        connection=con
    )
    con.close()
    return {
            "athletes": athletes,
            "championships": championships,
            "exercise_images": exercise_images,
            "exercise_instructions": exercise_instructions,
            "exercise_primary_muscles": exercise_primary_muscles,
            "exercise_secondary_muscles": exercise_secondary_muscles,
            "exercises": exercises,
            "practices": practices,
            "sports_with_exercises": sports_with_exercises,
            "sports": sports,
            "sport_exercises": sport_exercises,
            "teams": teams,
    }

