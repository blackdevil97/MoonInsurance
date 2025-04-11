from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection from environment variable
# mongo_uri = os.environ.get("MONGO_URI")
# mongo_uri = "mongodb://rajithawijesinghe74:ohClusterMoonInsuarancermooninsuarance@j7nq4hq.mongodb.net:27017/?retryWrites=true&w=majority&appName=ClusterMoonInsuarance"  # Replace with your MongoDB URI
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['MoonInsuranceDB']
agents_collection = db['Agents']

# Create agent
@app.route('/agent', methods=['POST'])
def create_agent():
    data = request.json
    if agents_collection.find_one({"agent_code": data["agent_code"]}):
        return jsonify({"error": "Agent already exists"}), 400
    agents_collection.insert_one(data)
    return jsonify({"message": "Agent created successfully"}), 201

# Get agent by code
@app.route('/agent/<agent_code>', methods=['GET'])
def get_agent(agent_code):
    agent = agents_collection.find_one({"agent_code": agent_code})
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    agent["_id"] = str(agent["_id"])
    return jsonify(agent), 200

# Update agent
@app.route('/agent/<agent_code>', methods=['PUT'])
def update_agent(agent_code):
    data = request.json
    result = agents_collection.update_one({"agent_code": agent_code}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Agent not found"}), 404
    return jsonify({"message": "Agent updated successfully"}), 200

# Delete agent
@app.route('/agent/<agent_code>', methods=['DELETE'])
def delete_agent(agent_code):
    result = agents_collection.delete_one({"agent_code": agent_code})
    if result.deleted_count == 0:
        return jsonify({"error": "Agent not found"}), 404
    return jsonify({"message": "Agent deleted successfully"}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Moon Insurance Agent Service is running 🚀"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
