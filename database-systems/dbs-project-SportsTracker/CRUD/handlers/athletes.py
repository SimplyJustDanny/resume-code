# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.athletes import AthletesDAO

class AthletesHandler:
    def getAllAthletesbad(self):
        #le falta el exercise

        s = {"id" : 123, "name" : "nasker", "gender" : "M", "venue" : "any"}
        
        s1 = {"id" : 124, "name" : "nasker", "gender" : "M", "venue" : "any"}
        result = [s,s1]
        result = [s,s1]
        return jsonify(result)
    

    def map_to_dict(self, athlete):
        result = {}
        # id, name, gender, venue, exercises
        result["id"] = athlete[0]
        result["name"] = athlete[1]
        result["age"] = athlete[2]
        result["gender"] = athlete[3]
        result["height"] = athlete[4]
        result["weight"] = athlete[5]
        return result

    def getAllAthletes(self):
        # data acces object, sabe como conectarse a la base de dato
        dao = AthletesDAO()
        Athletes_list = dao.getAllAthletes()
        result_list = []
        for athlete in Athletes_list:
            obj = self.map_to_dict(athlete)
            result_list.append(obj)
        return jsonify(result_list), 200
    

    def getAthleteById(self, id):
        dao = AthletesDAO()
        athlete = dao.getAthleteById(id)
        if not athlete:
            return jsonify("Not found"), 404
        else:
            result = self.map_to_dict(athlete)
            return jsonify(result), 200
    
    def insertAthlete(self, json):
        if "name" not in json or "age" not in json or "gender" not in json or "height" not in json or "weight" not in json or len(json) != 5:
            return jsonify("Invalid input"), 400
        name = json["name"]
        age = json["age"]
        gender = json["gender"]
        height = json["height"]
        weight = json["weight"]
        dao = AthletesDAO()
        if dao.IsAtheleteInDB(name, age, gender, height, weight) == 0:
            id = dao.insertAthlete(name, age, gender, height, weight)
            if not id:
                return jsonify("Server Error"), 500
            else:
                json["id"] = id
                return jsonify(json), 201
        else:
            return jsonify("Athlete already exists in DB"), 409

    def updateAthlete(self, id, json):
        if "name" not in json or "age" not in json or "gender" not in json or "height" not in json or "weight" not in json or len(json) != 5:
            return jsonify("Invalid input"), 400
        name = json["name"]
        age = json["age"]
        gender = json["gender"]
        height = json["height"]
        weight = json["weight"]
        dao = AthletesDAO()
        if dao.IsAtheleteInDB(name, age, gender, height, weight) == 0:
            athlete = dao.updateAthlete(id, name, age, gender, height, weight)
            if not athlete:
                return jsonify("Server Error"), 500
            else:
                json["id"] = athlete[0]
                return jsonify(json), 200
        else:
            return jsonify("Athlete already exists in DB"), 409

        
    def deleteAthlete(self, id):
        dao = AthletesDAO()
        rows = dao.deleteAthlete(id)
        if rows == 0:
            return jsonify("Referenced Table or Nonexistent"), 409
        else:
            return jsonify("No Content"), 204
