# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.primary_muscle import PrimaryMuscleDAO

class PrimaryMuscleHandler:
    def insertPrimaryMuscle(self, exercise_id, json):
        if "muscle_description" not in json or len(json) != 1:
            return jsonify("Invalid input"), 400 
        muscle_description = json["muscle_description"]
        dao = PrimaryMuscleDAO()
        id = dao.insertPrimaryMuscle(exercise_id, muscle_description)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json["muscle_id"] = id
            json["exercise_id"] = exercise_id
            return jsonify(json), 201

    
    def deletePrimaryMuscle(self, exercise_id, muscle_id):
        print("Handler")
        dao = PrimaryMuscleDAO()
        dao.deletePrimaryMuscle(exercise_id, muscle_id)
        return jsonify("No Content"), 204
