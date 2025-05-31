# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.exercise_instructions import ExerciseInstructionsDAO

class ExerciseInstructionsHandler:
    def insertExerciseInstructions(self, exercise_id, json):
        if "instruction_number" not in json or "description" not in json or len(json) != 2:
            return jsonify("Invalid input"), 400
        instruction_number = json["instruction_number"]
        description = json["description"]
        dao = ExerciseInstructionsDAO()
        id = dao.insertExerciseInstruction(exercise_id, instruction_number, description)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json["instruction_id"] = id
            json["exercise_id"] = exercise_id
            return jsonify(json), 201

    
    def deleteExerciseInstructions(sel, exercise_id, instruction_id):
        print("Handler")
        dao = ExerciseInstructionsDAO()
        dao.deleteExerciseInstructions(exercise_id, instruction_id)
        return jsonify("No Content"), 204
