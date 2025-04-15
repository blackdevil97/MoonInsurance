from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['MoonInsuranceDB']
sales_collection = db['Sales']

@app.route('/aggregation/best_teams', methods=['GET'])
def best_teams():
    pipeline = [
        {"$match": {"team_name": {"$ne": None}, "sales_value": {"$ne": None}}},
        {"$group": {"_id": "$team_name", "total_sales_value": {"$sum": "$sales_value"}}},
        {"$sort": {"total_sales_value": -1}}
    ]
    results = list(sales_collection.aggregate(pipeline))
    return jsonify({"best_performing_teams": results}), 200

@app.route('/aggregation/best_products', methods=['GET'])
def best_products():
    pipeline = [
        {"$match": {"product_name": {"$ne": None}, "sales_value": {"$ne": None}}},
        {"$group": {"_id": "$product_name", "total_sales_value": {"$sum": "$sales_value"}}},
        {"$sort": {"total_sales_value": -1}}
    ]
    results = list(sales_collection.aggregate(pipeline))
    return jsonify({"best_selling_products": results}), 200

@app.route('/aggregation/branch_performance', methods=['GET'])
def branch_performance():
    pipeline = [
        {"$match": {"branch_name": {"$ne": None}, "sales_value": {"$ne": None}}},
        {"$group": {"_id": "$branch_name", "total_sales_value": {"$sum": "$sales_value"}}},
        {"$sort": {"total_sales_value": -1}}
    ]
    results = list(sales_collection.aggregate(pipeline))
    return jsonify({"branch_sales_performance": results}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Moon Insurance Aggregator Service is running 🚀"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

# from flask import Flask, jsonify
# from pymongo import MongoClient
# import os

# app = Flask(__name__)
# mongo_uri = os.environ.get("MONGO_URI")
# client = MongoClient(mongo_uri)
# db = client['MoonInsuranceDB']
# sales_collection = db['Sales']

# @app.route('/aggregation/best_teams', methods=['GET'])
# def best_teams():
#     pipeline = [
#         {"$group": {"_id": "$team_name", "total_sales_value": {"$sum": "$sales_value"}}},
#         {"$sort": {"total_sales_value": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"best_performing_teams": results}), 200

# @app.route('/aggregation/best_products', methods=['GET'])
# def best_products():
#     pipeline = [
#         {"$group": {"_id": "$product_name", "total_sales_value": {"$sum": "$sales_value"}}},
#         {"$sort": {"total_sales_value": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"best_selling_products": results}), 200

# @app.route('/aggregation/branch_performance', methods=['GET'])
# def branch_performance():
#     pipeline = [
#         {"$group": {"_id": "$branch_name", "total_sales_value": {"$sum": "$sales_value"}}},
#         {"$sort": {"total_sales_value": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"branch_sales_performance": results}), 200

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Moon Insurance Aggregator Service is running 🚀"}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5004, debug=True)

# from flask import Flask, jsonify
# from pymongo import MongoClient
# from collections import Counter
# import os

# app = Flask(__name__)

# # MongoDB connection
# # mongo_uri = os.environ.get("MONGO_URI")
# # mongo_uri = "mongodb://rajithawijesinghe74:ohClusterMoonInsuarancermooninsuarance@j7nq4hq.mongodb.net:27017/?retryWrites=true&w=majority&appName=ClusterMoonInsuarance"  # Replace with your MongoDB URI
# mongo_uri = os.environ.get("MONGO_URI")
# client = MongoClient(mongo_uri)
# db = client['MoonInsuranceDB']
# sales_collection = db['Sales']

# # Best performing sales teams
# @app.route('/aggregation/best_teams', methods=['GET'])
# def best_teams():
#     pipeline = [
#         {"$group": {"_id": "$team_name", "total_sales": {"$sum": 1}}},
#         {"$sort": {"total_sales": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"best_performing_teams": results}), 200

# # Products that achieve the sales targets
# @app.route('/aggregation/best_products', methods=['GET'])
# def best_products():
#     pipeline = [
#         {"$group": {"_id": "$product_name", "total_sales": {"$sum": 1}}},
#         {"$sort": {"total_sales": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"best_selling_products": results}), 200

# # Branch-wise sales performance
# @app.route('/aggregation/branch_performance', methods=['GET'])
# def branch_performance():
#     pipeline = [
#         {"$group": {"_id": "$branch_name", "total_sales": {"$sum": 1}}},
#         {"$sort": {"total_sales": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"branch_sales_performance": results}), 200

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Moon Insurance Aggregator Service is running 🚀"}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5004, debug=True)
