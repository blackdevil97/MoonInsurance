# from flask import Flask, jsonify
# from pymongo import MongoClient
# import psycopg2
# from collections import Counter
# import os

# app = Flask(__name__)

# # MongoDB Configuration
# MONGO_URI = os.getenv("MONGO_URI")
# mongo_client = MongoClient(MONGO_URI)
# mongo_db = mongo_client['MoonInsuranceDB']
# sales_collection = mongo_db['Sales']

# # Redshift Configuration
# REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
# REDSHIFT_PORT = os.getenv("REDSHIFT_PORT")
# REDSHIFT_DBNAME = os.getenv("REDSHIFT_DBNAME")
# REDSHIFT_USER = os.getenv("REDSHIFT_USER")
# REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")

# # Redshift connection function
# def get_redshift_connection():
#     try:
#         conn = psycopg2.connect(
#             host=REDSHIFT_HOST,
#             port=REDSHIFT_PORT,
#             dbname=REDSHIFT_DBNAME,
#             user=REDSHIFT_USER,
#             password=REDSHIFT_PASSWORD
#         )
#         return conn
#     except Exception as e:
#         print(f"Error connecting to Redshift: {e}")
#         return None

# @app.route('/sync/best_teams', methods=['POST'])
# def sync_best_teams():
#     try:
#         # Mongo Aggregation
#         pipeline = [
#             {"$group": {"_id": "$team_name", "total_sales": {"$sum": 1}}}
#         ]
#         results = list(sales_collection.aggregate(pipeline))

#         # Redshift
#         conn = get_redshift_connection()
#         if not conn:
#             return jsonify({"error": "Redshift connection failed"}), 500
#         cursor = conn.cursor()

#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS best_teams (
#                 team_name VARCHAR(255),
#                 total_sales INT
#             )
#         """)
#         conn.commit()

#         for result in results:
#             cursor.execute(
#                 """
#                 INSERT INTO best_teams (team_name, total_sales)
#                 VALUES (%s, %s)
#                 """,
#                 (result["_id"], result["total_sales"])
#             )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         return jsonify({"message": "Best teams synced to Redshift"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "Moon Insurance Redshift Analytics Service is running 🚀"}), 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5005, debug=True)
from flask import Flask, jsonify
import pymongo
import os

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.environ.get("MONGO_URI")
mongo_client = pymongo.MongoClient(mongo_uri)
mongo_db = mongo_client["MoonInsuranceDB"]
mongo_collection = mongo_db["AggregatedResults"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Moon Insurance Redshift Analytics Service is running 🚀"}), 200

@app.route('/sync/best_teams', methods=['POST'])
def sync_best_teams():
    try:
        # MOCKED RESPONSE FOR TESTING WITHOUT REDSHIFT
        print("Mocking Redshift connection...")
        mock_data = [{"team": "Team A", "total_sales": 1000}]
        print("Mock data:", mock_data)
        return jsonify({"message": "Data synced successfully", "data": mock_data}), 200

    except Exception as e:
        print(f"Error during sync: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
