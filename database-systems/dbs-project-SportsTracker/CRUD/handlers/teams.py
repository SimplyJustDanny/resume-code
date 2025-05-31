# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.teams import TeamsDAO

class TeamsHandler:
    def map_to_dict(self, team):
        result = {}
        result["id"] = team[0]
        result["name"] = team[1]
        result["sport_id"] = team[2]
        return result
    
    def map_to_dict_champs(self, team):
        result = {}
        result["team_id"] = team[0]
        result["name"] = team[1]
        result["sport"] = team[2]
        result["championships_won"] = team[3]
        return result

    def map_to_dict_sportsdist(self, team):
        result = {}
        result["sport"] = team[0]
        result["team_count"] = team[1]
        return result

    def getAllTeams(self):
        # data acces object, sabe como conectarse a la base de dato
        dao = TeamsDAO()
        teams_list = dao.getAllTeams()
        result_list = []
        for team in teams_list:
            obj = self.map_to_dict(team)
            result_list.append(obj)
        return jsonify(result_list), 200
    

    def getTeamById(self, id):
        dao = TeamsDAO()
        team = dao.getTeamById(id)
        if not team:
            return jsonify("Not found"), 404
        else:
            result = self.map_to_dict(team)
            return jsonify(result), 200
    
    def insertTeam(self, json):
        keys = ["name", "sport_id"]
        for key in keys:
            if key not in json or len(json) != len(keys):
                return jsonify("Invalid input"), 400 
        name = json["name"]
        sport = json["sport_id"]
        dao = TeamsDAO()
        if dao.IsTeamInDB(name, sport) == 0:
            id = dao.insertTeam(name, sport)
            if not id:
                return jsonify("Server Error"), 500
            else:
                json["id"] = id
                return jsonify(json), 201
        else:
            return jsonify("Team already exists in DB"), 409

    
    def updateTeamById(self, id, json):
        keys = ["name", "sport_id"]
        for key in keys:
            if key not in json or len(json) != len(keys):
                return jsonify("Invalid input"), 400 
        name = json["name"]
        sport = json["sport_id"]
        dao = TeamsDAO()
        if dao.IsTeamInDB(name, sport) == 0:
            team = dao.updateTeamById(id, name, sport)
            if not team:
                return jsonify("Server Error"), 500
            else:
                return jsonify(self.map_to_dict(team)), 200
        else:
            return jsonify("Team already exists in DB"), 409

        
    def deleteTeam(self, id):
        dao = TeamsDAO()
        rows = dao.deleteTeam(id)
        if rows == 0:
            return jsonify("Referenced Table or Nonexistent"), 409
        else:
            return jsonify("No Content"), 204

    def getTopThreeTeams(self):
        # data acces object, sabe como conectarse a la base de dato
        dao = TeamsDAO()
        teams_list = dao.getTopThreeTeams()
        result_list = []
        for team in teams_list:
            obj = self.map_to_dict_champs(team)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getMostTeamsPerSport(self):
        # data acces object, sabe como conectarse a la base de dato
        dao = TeamsDAO()
        teams_list = dao.getMostTeamsPerSport()
        result_list = []
        for team in teams_list:
            obj = self.map_to_dict_sportsdist(team)
            result_list.append(obj)
        return jsonify(result_list), 200
