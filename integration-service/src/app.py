from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['MoonInsuranceDB']
sales_collection = db['Sales']

@app.route('/sales', methods=['POST'])
def receive_sales():
    data = request.json
    required_fields = ["agent_code", "product_name", "team_name", "branch_name", "sales_value"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 400
    try:
        data['sales_value'] = float(data['sales_value'])
        sales_collection.insert_one(data)
        return jsonify({"message": "Sales data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sales/agent/<agent_code>', methods=['GET'])
def get_sales_by_agent(agent_code):
    sales = list(sales_collection.find({"agent_code": agent_code}))
    for sale in sales:
        sale["_id"] = str(sale["_id"])
    return jsonify(sales), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Moon Insurance Integration Service is running 🚀"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)



# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# import os

# app = Flask(__name__)

# # MongoDB connection
# # mongo_uri = os.environ.get("MONGO_URI")
# # mongo_uri = "mongodb://rajithawijesinghe74:ohClusterMoonInsuarancermooninsuarance@j7nq4hq.mongodb.net:27017/?retryWrites=true&w=majority&appName=ClusterMoonInsuarance"  # Replace with your MongoDB URI
# mongo_uri = os.environ.get("MONGO_URI")
# client = MongoClient(mongo_uri)
# db = client['MoonInsuranceDB']
# sales_collection = db['Sales']

# # Endpoint to receive sales data
# @app.route('/sales', methods=['POST'])
# def receive_sales():
#     data = request.json
#     sales_collection.insert_one(data)
#     return jsonify({"message": "Sales data inserted successfully"}), 201

# # Get sales by agent code
# @app.route('/sales/agent/<agent_code>', methods=['GET'])
# def get_sales_by_agent(agent_code):
#     sales = list(sales_collection.find({"agent_code": agent_code}))
#     for sale in sales:
#         sale["_id"] = str(sale["_id"])
#     return jsonify(sales), 200

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Moon Insurance Integration Service is running 🚀"}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5002, debug=True)
