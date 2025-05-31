# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.sports import SportsDAO

class SportsHandler:
    def map_to_dict(self, sport):
        result = {}
        # id, name, gender, venue, exercises
        result["id"] = sport[0]
        result["name"] = sport[1]
        result["gender"] = sport[2]
        result["venue"] = sport[3]
        # TODO: Properly add exercises to queries
        # result["exercises"] = sport[4]
        return result

    def map_to_dict_popular(self, sport):
        result = {}
        result["sport"] = sport[0]
        result["athlete_count"] = sport[1]
        return result


    def getAllSports(self):
        # data acces object, sabe como conectarse a la base de dato
        dao = SportsDAO()
        sports_list = dao.getAllSports()
        result_list = []
        for sport in sports_list:
            obj = self.map_to_dict(sport)
            result_list.append(obj)
        return jsonify(result_list)
    

    def getSportById(self, id):
        dao = SportsDAO()
        val, sport = dao.getSportById(id)
        if not sport:
            return jsonify("Not found"), 404
        else:
            result = {
                    "exercises": []
            }
            for s in sport:
                result["id"] = s[0]
                result["name"] = s[1]
                result["gender"] = s[2]
                result["venue"] = s[3]
                if not val:
                    result["exercises"].append({
                        "id": s[4],
                        "name": s[5]
                    })

            return jsonify(result), 200
    
    def insertSport(self, json):
        if "name" not in json or "gender" not in json or "venue" not in json or len(json) != 3:
            return jsonify("Invalid input"), 400
        name = json["name"]
        gender = json["gender"]
        venue = json["venue"]
        dao = SportsDAO()
        id = dao.insertSport(name, gender, venue)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json["id"] = id
            return jsonify(json), 201
    
    def updateSport(self, id, json):
        if "name" not in json or "gender" not in json or "venue" not in json or len(json) != 3:
            return jsonify("Invalid input"), 400
        name = json["name"]
        gender = json["gender"]
        venue = json["venue"]
        dao = SportsDAO()
        sport = dao.updateSport(id, name, gender, venue)
        if not sport:
            return jsonify("Server Error"), 500
        else:
            json["id"] = sport[0]
            return jsonify(json), 200
        
    def deleteSport(self, id):
        dao = SportsDAO()
        rows = dao.deleteSport(id)
        if rows == 0:
            return jsonify("Referenced Table or Nonexistent"), 409
        else:
            return jsonify("No Content"), 204

    def addSportToExercise(self, exercise_id, sport_id):
        dao = SportsDAO()
        id = dao.addSportToExercise(exercise_id, sport_id)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json = {
                    "sport": sport_id,
                    "exercise": exercise_id
            }
            return jsonify(json), 201

    def removeSportFromExercise(self, exercise_id, sport_id):
        dao = SportsDAO()
        dao.removeSportFromExercise(exercise_id, sport_id)
        return jsonify("No Content"), 204

    def getMostPopularSports(self):
        dao = SportsDAO()
        sports_list = dao.getMostPopularSports()
        result_list = []
        for sport in sports_list:
            obj = self.map_to_dict_popular(sport)
            result_list.append(obj)
        return jsonify(result_list)
