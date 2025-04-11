from flask import Flask, jsonify
from pymongo import MongoClient
import psycopg2
import os

app = Flask(__name__)

# MongoDB Configuration
mongo_uri = os.environ.get("MONGO_URI")
# mongo_uri = "mongodb://rajithawijesinghe74:ohClusterMoonInsuarancermooninsuarance@j7nq4hq.mongodb.net:27017/?retryWrites=true&w=majority&appName=ClusterMoonInsuarance"  # Replace with your MongoDB URI
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["MoonInsuranceDB"]

sales_collection = mongo_db["Sales"]

# Redshift Configuration
REDSHIFT_HOST = os.environ.get("REDSHIFT_HOST")
REDSHIFT_PORT = int(os.environ.get("REDSHIFT_PORT", 5439))
REDSHIFT_DBNAME = os.environ.get("REDSHIFT_DBNAME")
REDSHIFT_USER = os.environ.get("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.environ.get("REDSHIFT_PASSWORD")

# Function to connect to Redshift
def get_redshift_connection():
    try:
        conn = psycopg2.connect(
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT,
            dbname=REDSHIFT_DBNAME,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD
        )
        print("✅ Connected to Redshift successfully!")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Redshift: {e}")
        return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Moon Insurance Redshift Analytics Service is running 🚀"}), 200

# 1️⃣ Best Performing Sales Teams
@app.route('/sync/best_teams', methods=['POST'])
def sync_best_teams():
    try:
        pipeline = [
            {"$group": {"_id": "$team_name", "total_sales": {"$sum": 1}}},
            {"$sort": {"total_sales": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        print("🔍 Aggregated Best Teams:", results)

        conn = get_redshift_connection()
        if not conn:
            return jsonify({"error": "Redshift connection failed"}), 500
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS best_teams (
                team_name VARCHAR(255),
                total_sales INT
            )
        """)
        conn.commit()

        for result in results:
            cursor.execute(
                """
                INSERT INTO best_teams (team_name, total_sales)
                VALUES (%s, %s)
                """,
                (result["_id"], result["total_sales"])
            )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Best teams synced to Redshift ✅", "data": results}), 200

    except Exception as e:
        print(f"❌ Error in sync_best_teams: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 2️⃣ Products Achieving Sales Targets
@app.route('/sync/products_achieving_targets', methods=['POST'])
def sync_products_achieving_targets():
    try:
        target_sales = 10  # Example threshold, can be dynamic
        pipeline = [
            {"$group": {"_id": "$product_name", "total_sales": {"$sum": 1}}},
            {"$match": {"total_sales": {"$gte": target_sales}}},
            {"$sort": {"total_sales": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        print("🔍 Aggregated Products Achieving Targets:", results)

        conn = get_redshift_connection()
        if not conn:
            return jsonify({"error": "Redshift connection failed"}), 500
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products_achieving_targets (
                product_name VARCHAR(255),
                total_sales INT
            )
        """)
        conn.commit()

        for result in results:
            cursor.execute(
                """
                INSERT INTO products_achieving_targets (product_name, total_sales)
                VALUES (%s, %s)
                """,
                (result["_id"], result["total_sales"])
            )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Products achieving targets synced to Redshift ✅", "data": results}), 200

    except Exception as e:
        print(f"❌ Error in sync_products_achieving_targets: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 3️⃣ Branch Wise Sales Performance
@app.route('/sync/branch_wise_performance', methods=['POST'])
def sync_branch_wise_performance():
    try:
        pipeline = [
            {"$group": {"_id": "$branch", "total_sales": {"$sum": 1}}},
            {"$sort": {"total_sales": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        print("🔍 Aggregated Branch Wise Sales Performance:", results)

        conn = get_redshift_connection()
        if not conn:
            return jsonify({"error": "Redshift connection failed"}), 500
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS branch_wise_sales_performance (
                branch_name VARCHAR(255),
                total_sales INT
            )
        """)
        conn.commit()

        for result in results:
            cursor.execute(
                """
                INSERT INTO branch_wise_sales_performance (branch_name, total_sales)
                VALUES (%s, %s)
                """,
                (result["_id"], result["total_sales"])
            )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Branch wise sales performance synced to Redshift ✅", "data": results}), 200

    except Exception as e:
        print(f"❌ Error in sync_branch_wise_performance: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
