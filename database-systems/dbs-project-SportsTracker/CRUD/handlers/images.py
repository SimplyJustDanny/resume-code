# Convierte de el dictionary de python y lo convierte en javascript
from flask import jsonify
from dao.images import ImageDAO

class ImageHandler:
    def insertImage(self, exercise_id, json):
        if "path" not in json or len(json) != 1:
            return jsonify("Invalid input"), 400 
        path = json["path"]
        dao = ImageDAO()
        id = dao.insertImage(exercise_id, path)
        if not id:
            return jsonify("Server Error"), 500
        else:
            json["image_id"] = id
            json["exercise_id"] = exercise_id
            return jsonify(json), 201

    
    def deleteImage(self, exercise_id, image_id):
        dao = ImageDAO()
        dao.deleteImage(exercise_id, image_id)
        return jsonify("No Content"), 204
