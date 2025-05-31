from flask import jsonify
from dao.championships import ChampionshipsDAO

class ChampionshipsHandler:

    def map_to_dict(self, championship):
        result = {}
        result["id"] = championship[0]
        result["name"] = championship[1]
        result["winner_team"] = championship[2]
        result["year"] = championship[3]
        return result

    def map_to_dict_mostwon(self, championship):
        result = {}
        result["team_id"] = championship[0]
        result["name"] = championship[1]
        result["total_wins"] = championship[2]
        return result

    def getAllChampionships(self):
        dao = ChampionshipsDAO()
        Championships_list = dao.getAllChampionships()
        result_list = []
        for championship in Championships_list:
            obj = self.map_to_dict(championship)
            result_list.append(obj)
        return jsonify(result_list), 200
    

    def getChampionshipById(self, id):
        dao = ChampionshipsDAO()
        championship = dao.getChampionshipById(id)
        if not championship:
            return jsonify("Not found"), 404
        else:
            print()
            print()
            print(championship)
            print()
            print()
            result = self.map_to_dict(championship[0])
            result["winner_team"] = {
                    "team_id": championship[1][0],
                    "name": championship[1][1]
            }
            return jsonify(result), 200
    
    def insertChampionship(self, json):
        keys = ["name", "winner_team_id", "year"]
        for key in keys:
            if key not in json or len(json) != len(keys):
                return jsonify("Invalid input"), 400 
        name = json["name"]
        winner_team = json["winner_team_id"]
        year = json["year"]
        dao = ChampionshipsDAO()
        id = dao.insertChampionship(name, winner_team, year)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json["id"] = id
            return jsonify(json), 201
    
    def updateChampionship(self, id, json):
        keys = ["name", "winner_team_id", "year"]
        for key in keys:
            if key not in json or len(json) != len(keys):
                return jsonify("Invalid input"), 400 
        name = json["name"]
        winner_team = json["winner_team_id"]
        year = json["year"]
        dao = ChampionshipsDAO()
        championship = dao.updateChampionship(id, name, winner_team, year)
        if not championship:
            return jsonify("Server Error"), 500
        else:
            json["id"] = championship
            return jsonify(json), 200
        
    def deleteChampionship(self, id):
        dao = ChampionshipsDAO()
        dao.deleteChampionship(id)
        return jsonify("No Content"), 204

    def getMostWonChampionships(self):
        dao = ChampionshipsDAO()
        Championships_list = dao.getMostWonChampionships()
        result_list = []
        for championship in Championships_list:
            obj = self.map_to_dict_mostwon(championship)
            result_list.append(obj)
        return jsonify(result_list), 200
