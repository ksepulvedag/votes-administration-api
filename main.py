from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
from Controllers.ControllerCandidate import ControllerCandidate
from Controllers.ControllerTable import ControllerTable
from Controllers.ControllerParty import ControllerParty
from Controllers.ControllerResult import ControllerResult

app=Flask(__name__)
cors = CORS(app)

controller_candidate = ControllerCandidate()
controller_table = ControllerTable()
controller_party = ControllerParty()
controller_result = ControllerResult()

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

############ Candidate ############

# List all candidates
@app.route("/candidate",methods=['GET'])
def get_candidate():
    json=controller_candidate.index()
    return jsonify(json)

# Create a new candidate
@app.route("/candidate",methods=['POST'])
def create_candidate():
    data = request.get_json()
    json=controller_candidate.create(data)
    return jsonify(json)

# list one candidate by id
@app.route("/candidate/<string:id>",methods=['GET'])
def get_candidate_by_id(id):
    json=controller_candidate.show(id)
    return jsonify(json)

# Update one candidate's info by id
@app.route("/candidate/<string:id>",methods=['PUT'])
def edit_candidate(id):
    data = request.get_json()
    json=controller_candidate.update(id,data)
    return jsonify(json)

# Delete one candidate by id
@app.route("/candidate/<string:id>",methods=['DELETE'])
def delete_candidate(id):
    json=controller_candidate.delete(id)
    return jsonify(json)

@app.route("/candidate/<string:candidate_id>/party/<string:party_id>",methods=['PUT'])
def assign_candidate_party(candidate_id,party_id):
    json=controller_candidate.assignParty(candidate_id,party_id)
    return jsonify(json)

############ Table ############

# List all tables
@app.route("/table",methods=['GET'])
def get_table():
    json=controller_table.index()
    return jsonify(json)

# Create a new table
@app.route("/table",methods=['POST'])
def create_table():
    data = request.get_json()
    json=controller_table.create(data)
    return jsonify(json)

# list one table by id
@app.route("/table/<string:id>",methods=['GET'])
def get_table_by_id(id):
    json=controller_table.show(id)
    return jsonify(json)

# Update one table's info by id
@app.route("/table/<string:id>",methods=['PUT'])
def edit_table(id):
    data = request.get_json()
    json=controller_table.update(id,data)
    return jsonify(json)

# Delete one table by id
@app.route("/table/<string:id>",methods=['DELETE'])
def delete_table(id):
    json=controller_table.delete(id)
    return jsonify(json)

############ Political Party ############

# List all political parties
@app.route("/party",methods=['GET'])
def get_party():
    json=controller_party.index()
    return jsonify(json)

# Create a new party
@app.route("/party",methods=['POST'])
def create_party():
    data = request.get_json()
    json=controller_party.create(data)
    return jsonify(json)

# list one party by id
@app.route("/party/<string:id>",methods=['GET'])
def get_party_by_id(id):
    json=controller_party.show(id)
    return jsonify(json)

# Update one party's info by id
@app.route("/party/<string:id>",methods=['PUT'])
def edit_party(id):
    data = request.get_json()
    json=controller_party.update(id,data)
    return jsonify(json)

# Delete one party by id
@app.route("/party/<string:id>",methods=['DELETE'])
def delete_party(id):
    json=controller_party.delete(id)
    return jsonify(json)

############ Result ############

# List all results
@app.route("/result",methods=['GET'])
def get_result():
    json=controller_result.index()
    return jsonify(json)

# Create a new result
@app.route("/result/candidate/<string:candidate_id>/table/<string:table_id>",methods=['POST'])
def create_result(candidate_id,table_id):
    data = request.get_json()
    json=controller_result.create(data,candidate_id,table_id)
    return jsonify(json)

# list one result by id
@app.route("/result/<string:id>",methods=['GET'])
def get_result_by_id(id):
    json=controller_result.show(id)
    return jsonify(json)

# Update one result's info by id
@app.route("/result/<string:id>",methods=['PUT'])
def edit_result(id):
    data = request.get_json()
    json=controller_result.update(id,data)
    return jsonify(json)

# Delete one result by id
@app.route("/result/<string:id>",methods=['DELETE'])
def delete_result(id):
    json=controller_result.delete(id)
    return jsonify(json)

# List votes per table
@app.route("/result/table/<string:table_id>",methods=['GET'])
def show_votes_per_table(table_id):
    json=controller_result.list_votes_per_table(table_id)
    return jsonify(json)

# List most voted candidate per table
@app.route("/result/table/most_voted",methods=['GET'])
def show_most_voted_per_table():
    json=controller_result.most_voted_per_table()
    return jsonify(json)

# List average votes per table
@app.route("/result/table/avg_voted/<string:table_id>",methods=['GET'])
def show_average_votes_per_table(table_id):
    json=controller_result.average_votes_per_table(table_id)
    return jsonify(json)


# Main function
if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])