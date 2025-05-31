from flask import Flask, jsonify, request
from flask_cors import CORS

#import the handlers
from handlers.sports import SportsHandler
from handlers.athletes import AthletesHandler
from handlers.exercises import ExercisesHandler
from handlers.teams import TeamsHandler
from handlers.primary_muscle import PrimaryMuscleHandler
from handlers.secondary_muscle import SecondaryMuscleHandler
from handlers.images import ImageHandler
from handlers.exercise_instructions import ExerciseInstructionsHandler
from handlers.championships import ChampionshipsHandler

#para correr la pagina, se para en el file , run code, en el terminal marca el link
# objeto de flask 
app  = Flask(__name__)
# wrap a CORS para que acepte request de diferentes lugares 
CORS(app)



@app.route('/')
def index():
    return "Welcome to the main page."



# Athlete
@app.route('/athlete/<int:id>', methods = ["GET", "PUT", "DELETE"])
def handleAthleteById(id):
    if request.method == "GET":
        return AthletesHandler().getAthleteById(id)
    elif request.method == "PUT":
        return AthletesHandler().updateAthlete(id, request.json)
    elif request.method == "DELETE":
        return AthletesHandler().deleteAthlete(id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/athlete', methods = ["POST" , "GET"])
def handleAthlete():
    if request.method == "GET":
        return AthletesHandler().getAllAthletes()
    elif request.method == "POST":
        return AthletesHandler().insertAthlete(request.json)
    else:
        return jsonify("Unsupported Method"), 405

# Sport
@app.route('/sport/<int:id>', methods = ["GET", "PUT", "DELETE"])
def handleSportsById(id):
    if request.method == "GET":
        return SportsHandler().getSportById(id)
    elif request.method == "PUT":
        return SportsHandler().updateSport(id, request.json)
    elif request.method == "DELETE":
        return SportsHandler().deleteSport(id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/sport', methods = ["POST" , "GET"])
def handleSports():
    if request.method == "GET":
        return SportsHandler().getAllSports()
    elif request.method == "POST":
        return SportsHandler().insertSport(request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/sports/popularity', methods = ["GET"])
def handleSportsByPopularity():
    if request.method == "GET":
        return SportsHandler().getMostPopularSports()
    else:
        return jsonify("Unsupported Method"), 405

# Teams
@app.route('/team/<int:id>', methods = ["GET", "PUT", "DELETE"])
def handleTeamById(id):
    print("GO!")
    if request.method == "GET":
        return TeamsHandler().getTeamById(id)
    elif request.method == "PUT":
        return TeamsHandler().updateTeamById(id, request.json)
    elif request.method == "DELETE":
        return TeamsHandler().deleteTeam(id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/team', methods = ["POST" , "GET"])
def handleTeams():
    if request.method == "GET":
        return TeamsHandler().getAllTeams()
    elif request.method == "POST":
        return TeamsHandler().insertTeam(request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/teams/top-teams', methods = ["GET"])
def handleTopThreeTeams():
    if request.method == "GET":
        return TeamsHandler().getTopThreeTeams()
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/teams/sports-distribution', methods = ["GET"])
def handleMostTeamsPerSport():
    if request.method == "GET":
        return TeamsHandler().getMostTeamsPerSport()
    else:
        return jsonify("Unsupported Method"), 405

# Exercise
@app.route('/exercise', methods = ["POST" , "GET"])
def handleExercise():
    if request.method == "GET":
        return ExercisesHandler().getAllExercises()
    elif request.method == "POST":
        return ExercisesHandler().insertExercise(request.json)
    else:
        return jsonify("Unsupported Method"), 405
 
@app.route('/exercise/<int:id>', methods = ["GET", "PUT", "DELETE"])
def handleExerciseById(id):
    if request.method == "GET":
        return ExercisesHandler().getExerciseById(id)
    elif request.method == "PUT":
        return ExercisesHandler().updateExercise(id, request.json)
    elif request.method == "DELETE":
        return ExercisesHandler().deleteExercise(id)

@app.route('/exercise/<int:exercise_id>/instruction', methods = ["POST"])
def handleExerciseInstructions(exercise_id):
    if request.method == "POST":
        return ExerciseInstructionsHandler().insertExerciseInstructions(exercise_id, request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercise/<int:exercise_id>/instruction/<int:instruction_id>', methods = ["DELETE"])
def handleExerciseInstructionsById(exercise_id,instruction_id):
    if request.method == "DELETE":
        return ExerciseInstructionsHandler().deleteExerciseInstructions(exercise_id, instruction_id)
    else:
        return jsonify("Unsupported Method"), 405   

@app.route('/exercise/<int:id>/primary-muscle', methods = ["POST"])
def handlePrimaryMuscleRelationship(id):
    if request.method == "POST":
        return PrimaryMuscleHandler().insertPrimaryMuscle(id, request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercise/<int:exercise_id>/primary-muscle/<int:muscle_id>', methods = ["DELETE"])
def handlePrimaryMuscleDelete(exercise_id, muscle_id):
    print("Starting delete")
    if request.method == "DELETE":
        return PrimaryMuscleHandler().deletePrimaryMuscle(exercise_id, muscle_id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercise/<int:id>/secondary-muscle', methods = ["POST"])
def handleSecondaryMuscleRelationship(id):
    if request.method == "POST":
        return SecondaryMuscleHandler().insertSecondaryMuscle(id, request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercise/<int:exercise_id>/secondary-muscle/<int:muscle_id>', methods = ["DELETE"])
def handleSecondaryMuscleDelete(exercise_id, muscle_id):
    print("Starting delete")
    if request.method == "DELETE":
        return SecondaryMuscleHandler().deleteSecondaryMuscle(exercise_id, muscle_id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercise/<int:exercise_id>/image', methods = ["POST"])
def handleImageAdd(exercise_id):
    if request.method == "POST":
        return ImageHandler().insertImage(exercise_id, request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercise/<int:exercise_id>/image/<int:image_id>', methods = ["DELETE"])
def handleImageDelete(exercise_id, image_id):
    print("Starting delete")
    if request.method == "DELETE":
        return ImageHandler().deleteImage(exercise_id, image_id)
    else:
        return jsonify("Unsupported Method"), 405
    
@app.route("/exercise/<int:exercise_id>/sport/<int:sport_id>", methods = ["POST", "DELETE"])
def handleExerciseAddOrRemoveSport(exercise_id, sport_id):
    if request.method == "POST":
        return SportsHandler().addSportToExercise(exercise_id, sport_id)
    if request.method == "DELETE":
        return SportsHandler().removeSportFromExercise(exercise_id, sport_id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercises/most-performed', methods = ["GET"])
def handleTopFiveExercises():
    if request.method == "GET":
        return ExercisesHandler().getTopFiveExercises()
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercises/muscle-group', methods = ["GET"])
def handleExercisesByMuscle():
    if len(request.args) == 0:
        return jsonify("Missing Parameters"), 400
    muscle_args = request.args.to_dict()
    if request.method == "GET":
        return ExercisesHandler().getExercisesByMuscle(muscle_args["muscle"])
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/exercises/most-complex', methods = ["GET"])
def handleMostComplexExercises():
    if request.method == "GET":
        return ExercisesHandler().getMostComplexExercises()
    else:
        return jsonify("Unsupported Method"), 405

# Championship
@app.route('/championship', methods = ["GET", "POST"])
def handleChampionshipGetAllOrInsert():
    if request.method == "GET":
        return ChampionshipsHandler().getAllChampionships()
    elif request.method == "POST":
        return ChampionshipsHandler().insertChampionship(request.json)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/championship/<int:id>', methods = ["GET", "PUT", "DELETE"])
def handleChampionshipById(id):
    if request.method == "GET":
        return ChampionshipsHandler().getChampionshipById(id)
    elif request.method == "PUT":
        return ChampionshipsHandler().updateChampionship(id, request.json)
    elif request.method == "DELETE":
        return ChampionshipsHandler().deleteChampionship(id)
    else:
        return jsonify("Unsupported Method"), 405

@app.route('/championships/most-wins', methods = ["GET"])
def handleMostWonChampionships():
    if request.method == "GET":
        return ChampionshipsHandler().getMostWonChampionships()
    else:
        return jsonify("Unsupported Method"), 405



if __name__ == '__main__':
    app.run(debug=True)
