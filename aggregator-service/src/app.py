from flask import Flask, jsonify
from pymongo import MongoClient
import psycopg2
import os
import sys

app = Flask(__name__)

# ========================================================
# ✅ Step 1: Load Environment Variables and Setup MongoDB
# ========================================================

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ ERROR: MONGO_URI not set!")
    sys.exit(1)

try:
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client["MoonInsuranceDB"]
    sales_collection = mongo_db["Sales"]
    print("✅ Connected to MongoDB!")
except Exception as e:
    print(f"❌ ERROR connecting to MongoDB: {e}")
    sys.exit(1)

# ========================================================
# ✅ Step 2: Setup Redshift Connection
# ========================================================

REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_PORT = int(os.getenv("REDSHIFT_PORT", 5439))
REDSHIFT_DBNAME = os.getenv("REDSHIFT_DBNAME")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")

def get_redshift_connection():
    try:
        conn = psycopg2.connect(
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT,
            dbname=REDSHIFT_DBNAME,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD
        )
        print("✅ Connected to Redshift!")
        return conn
    except Exception as e:
        print(f"❌ ERROR connecting to Redshift: {e}")
        return None

# ========================================================
# ✅ Health Check
# ========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Moon Insurance Redshift Analytics Service is running 🚀"}), 200

# ========================================================
# ✅ Best Teams Sync
# ========================================================

@app.route('/sync/best_teams', methods=['POST'])
def sync_best_teams():
    try:
        pipeline = [
            {"$match": {"team_name": {"$ne": None}, "sales_value": {"$ne": None}}},
            {"$group": {"_id": "$team_name", "total_sales_value": {"$sum": "$sales_value"}}},
            {"$sort": {"total_sales_value": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))

        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS best_teams (
                team_name VARCHAR(255),
                total_sales_value FLOAT
            );
            TRUNCATE TABLE best_teams;
        """)
        for result in results:
            cursor.execute("""
                INSERT INTO best_teams (team_name, total_sales_value)
                VALUES (%s, %s)
            """, (result["_id"], result["total_sales_value"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Best teams synced to Redshift ✅", "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================================================
# ✅ Products Achieving Targets Sync
# ========================================================

@app.route('/sync/products_achieving_targets', methods=['POST'])
def sync_products_achieving_targets():
    try:
        pipeline = [
            {"$match": {"product_name": {"$ne": None}, "sales_value": {"$ne": None}}},
            {"$group": {"_id": "$product_name", "total_sales_value": {"$sum": "$sales_value"}}},
            {"$match": {"total_sales_value": {"$gte": 50000}}},
            {"$sort": {"total_sales_value": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))

        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products_achieving_targets (
                product_name VARCHAR(255),
                total_sales_value FLOAT
            );
            TRUNCATE TABLE products_achieving_targets;
        """)
        for result in results:
            cursor.execute("""
                INSERT INTO products_achieving_targets (product_name, total_sales_value)
                VALUES (%s, %s)
            """, (result["_id"], result["total_sales_value"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Products achieving targets synced to Redshift ✅", "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================================================
# ✅ Branch Wise Performance Sync
# ========================================================

@app.route('/sync/branch_wise_performance', methods=['POST'])
def sync_branch_wise_performance():
    try:
        pipeline = [
            {"$match": {"branch_name": {"$ne": None}, "sales_value": {"$ne": None}}},
            {"$group": {"_id": "$branch_name", "total_sales_value": {"$sum": "$sales_value"}}},
            {"$sort": {"total_sales_value": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))

        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS branch_wise_sales_performance (
                branch_name VARCHAR(255),
                total_sales_value FLOAT
            );
            TRUNCATE TABLE branch_wise_sales_performance;
        """)
        for result in results:
            cursor.execute("""
                INSERT INTO branch_wise_sales_performance (branch_name, total_sales_value)
                VALUES (%s, %s)
            """, (result["_id"], result["total_sales_value"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Branch wise performance synced to Redshift ✅", "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================================================
# ✅ Start Server
# ========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)

# from flask import Flask, jsonify
# from pymongo import MongoClient
# import os

# app = Flask(__name__)
# mongo_uri = os.environ.get("MONGO_URI")
# client = MongoClient(mongo_uri)
# db = client['MoonInsuranceDB']
# sales_collection = db['Sales']

# @app.route('/sync/best_teams', methods=['POST'])
# def sync_best_teams():
#     try:
#         pipeline = [
#             {"$match": {"team_name": {"$ne": None}, "sales_value": {"$ne": None}}},
#             {"$group": {"_id": "$team_name", "total_sales_value": {"$sum": "$sales_value"}}},
#             {"$sort": {"total_sales_value": -1}}
#         ]
#         results = list(sales_collection.aggregate(pipeline))
#         print(f"🔍 Aggregated Best Teams: {results}")

#         conn = get_redshift_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS best_teams (
#                 team_name VARCHAR(255),
#                 total_sales_value FLOAT
#             );
#             TRUNCATE TABLE best_teams;
#         """)
#         for result in results:
#             cursor.execute("""
#                 INSERT INTO best_teams (team_name, total_sales_value)
#                 VALUES (%s, %s)
#             """, (result["_id"], result["total_sales_value"]))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Best teams synced to Redshift ✅", "data": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/sync/products_achieving_targets', methods=['POST'])
# def sync_products_achieving_targets():
#     try:
#         pipeline = [
#             {"$match": {"product_name": {"$ne": None}, "sales_value": {"$ne": None}}},
#             {"$group": {"_id": "$product_name", "total_sales_value": {"$sum": "$sales_value"}}},
#             {"$match": {"total_sales_value": {"$gte": 50000}}},
#             {"$sort": {"total_sales_value": -1}}
#         ]
#         results = list(sales_collection.aggregate(pipeline))
#         print(f"🔍 Aggregated Products Achieving Targets: {results}")

#         conn = get_redshift_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS products_achieving_targets (
#                 product_name VARCHAR(255),
#                 total_sales_value FLOAT
#             );
#             TRUNCATE TABLE products_achieving_targets;
#         """)
#         for result in results:
#             cursor.execute("""
#                 INSERT INTO products_achieving_targets (product_name, total_sales_value)
#                 VALUES (%s, %s)
#             """, (result["_id"], result["total_sales_value"]))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Products achieving targets synced to Redshift ✅", "data": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/sync/branch_wise_performance', methods=['POST'])
# def sync_branch_wise_performance():
#     try:
#         pipeline = [
#             {"$match": {"branch_name": {"$ne": None}, "sales_value": {"$ne": None}}},
#             {"$group": {"_id": "$branch_name", "total_sales_value": {"$sum": "$sales_value"}}},
#             {"$sort": {"total_sales_value": -1}}
#         ]
#         results = list(sales_collection.aggregate(pipeline))
#         print(f"🔍 Aggregated Branch Wise Performance: {results}")

#         conn = get_redshift_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS branch_wise_sales_performance (
#                 branch_name VARCHAR(255),
#                 total_sales_value FLOAT
#             );
#             TRUNCATE TABLE branch_wise_sales_performance;
#         """)
#         for result in results:
#             cursor.execute("""
#                 INSERT INTO branch_wise_sales_performance (branch_name, total_sales_value)
#                 VALUES (%s, %s)
#             """, (result["_id"], result["total_sales_value"]))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Branch wise performance synced to Redshift ✅", "data": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/aggregation/best_products', methods=['GET'])
# def best_products():
#     pipeline = [
#         {"$match": {"product_name": {"$ne": None}, "sales_value": {"$ne": None}}},
#         {"$group": {"_id": "$product_name", "total_sales_value": {"$sum": "$sales_value"}}},
#         {"$sort": {"total_sales_value": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"best_selling_products": results}), 200

# @app.route('/aggregation/branch_performance', methods=['GET'])
# def branch_performance():
#     pipeline = [
#         {"$match": {"branch_name": {"$ne": None}, "sales_value": {"$ne": None}}},
#         {"$group": {"_id": "$branch_name", "total_sales_value": {"$sum": "$sales_value"}}},
#         {"$sort": {"total_sales_value": -1}}
#     ]
#     results = list(sales_collection.aggregate(pipeline))
#     return jsonify({"branch_sales_performance": results}), 200

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
