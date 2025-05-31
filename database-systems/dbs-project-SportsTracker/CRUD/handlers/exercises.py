# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.exercises import ExercisesDAO

class ExercisesHandler:

    def map_to_dict(self, exercise):
        result = {}
        result["id"] = exercise[0]
        result["alter_id"] = exercise[1]
        result["force"] = exercise[2]
        result["level"] = exercise[3]
        result["mechanic"] = exercise[4]
        result["equipment"] = exercise[5]
        result["category"] = exercise[6]
        return result

    def map_to_dict_topfive(self, exercise):
        result = {}
        result["exercise_id"] = exercise[0]
        result["name"] = exercise[1]
        result["sports_related"] = exercise[2]
        return result

    def map_to_dict_muscles(self, exercise):
        result = {}
        result["exercise_id"] = exercise[0]
        result["name"] = exercise[1]
        return result

    def map_to_dict_complex(self, exercise):
        result = {}
        result["exercise_id"] = exercise[0]
        result["name"] = exercise[1]
        result["muscle_groups"] = exercise[2]
        return result

    def getAllExercises(self):
        dao = ExercisesDAO()
        Exercises_list = dao.getAllExercises()
        result_list = []
        for exercise in Exercises_list:
            obj = self.map_to_dict(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200
    
    def insertExercise(self, json):
        keys = ["name", "alter_id", "force", "level", "mechanic", "equipment", "category"]
        for key in keys:
            if key not in json or len(json) != len(keys):
                return jsonify("Invalid input"), 400 
        
        name = json["name"]
        alter_id = json["alter_id"]
        force = json["force"]
        level = json["level"]
        mechanic = json["mechanic"]
        equipment = json["equipment"]
        category = json["category"]
        # name = json["name"]
        # age = json["age"]
        # gender = json["gender"]
        # height = json["height"]
        # weight = json["weight"]
        dao = ExercisesDAO()
        id = dao.insertExercise(name, alter_id, force, level, mechanic, equipment, category)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json["id"] = id
            return jsonify(json), 201


    def getExerciseById(self, id):
        dao = ExercisesDAO()
        exercise = dao.getExerciseById(id)
        if not exercise:
            return jsonify("Not found"), 404
        else:
            # result = self.map_to_dict(exercise)

                # exercises.id, name, alter_id, force, level, mechanic, equipment, category, 
                # exercise_instructions.id, instruction_number, instruction, 
                # image_path,
                # exercise_primary_muscles.muscle,
                # exercise_secondary_muscles.muscle 
            print(exercise)
            exercise_json = {
                    "id": exercise[0][0][0],
                    "name": exercise[0][0][1],
                    "alter_id": exercise[0][0][2],
                    "force": exercise[0][0][3],
                    "level": exercise[0][0][4],
                    "mechanic": exercise[0][0][5],
                    "equipment": exercise[0][0][6],
                    "category": exercise[0][0][7],
                    "instructions": [],
                    "images": [],
                    "primary_muscles": [],
                    "secondary_muscles": [],
            }
            for row in exercise[1]:
                exercise_json["instructions"].append({
                    "instruction_id": row[0],
                    "instruction_number": row[1],
                    "description": row[2]
                })
            for row in exercise[2]:
                exercise_json["images"].append({
                    "image_id": row[0],
                    "path": row[1],
                })
            for row in exercise[3]:
                exercise_json["primary_muscles"].append({
                    "muscle_id": row[0],
                    "name": row[1],
                })
            for row in exercise[4]:
                exercise_json["secondary_muscles"].append({
                    "muscle_id": row[0],
                    "name": row[1],
                })


            result = exercise_json
            return jsonify(result), 200
    
    def updateExercise(self, id, json):
        keys = ["name", "alter_id", "force", "level", "mechanic", "equipment", "category"]
        for key in keys:
            if key not in json or len(json) != len(keys):
                return jsonify("Invalid input"), 400 
        name = json["name"]
        alter_id = json["alter_id"]
        force = json["force"]
        level = json["level"]
        mechanic = json["mechanic"]
        equipment = json["equipment"]
        category = json["category"]
        dao = ExercisesDAO()
        exercise = dao.updateExercise(id, name, alter_id, force, level, mechanic, equipment, category)
        if not exercise:
            return jsonify("Server Error"), 500
        else:
            json["id"] = exercise
            return jsonify(json), 200

    def deleteExercise(self, id):
        dao = ExercisesDAO()
        rows = dao.deleteExercise(id)
        if rows == 0:
            return jsonify("Referenced Table or Nonexistent"), 409
        else:
            return jsonify("No Content"), 204

    def getTopFiveExercises(self):
        dao = ExercisesDAO()
        Exercises_list = dao.getTopFiveExercises()
        result_list = []
        for exercise in Exercises_list:
            obj = self.map_to_dict_topfive(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getExercisesByMuscle(self, muscle):
        dao = ExercisesDAO()
        Exercises_list = dao.getExercisesByMuscle(muscle)
        result_list = []
        for exercise in Exercises_list:
            obj = self.map_to_dict_muscles(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getMostComplexExercises(self):
        dao = ExercisesDAO()
        Exercises_list = dao.getMostComplexExercises()
        result_list = []
        for exercise in Exercises_list:
            obj = self.map_to_dict_complex(exercise)
            result_list.append(obj)
        return jsonify(result_list), 200
