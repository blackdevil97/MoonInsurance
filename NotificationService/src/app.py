from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['MoonInsuranceDB']
sales_collection = db['Sales']

SALES_TARGET = 5  # Sample target (you can adjust)

# Endpoint to check if sales target is met for agent
@app.route('/notification/check_target/<agent_code>', methods=['GET'])
def check_sales_target(agent_code):
    count = sales_collection.count_documents({"agent_code": agent_code})
    if count >= SALES_TARGET:
        # Simulate notification
        print(f"🎉 Notification: Agent {agent_code} has achieved sales target with {count} sales!")
        return jsonify({"message": f"Agent {agent_code} has achieved sales target!"}), 200
    else:
        return jsonify({"message": f"Agent {agent_code} has {count} sales. Target not reached yet."}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Moon Insurance Notification Service is running 🚀"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
