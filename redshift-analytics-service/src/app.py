from flask import Flask, jsonify
from pymongo import MongoClient
import psycopg2
import os
import sys

app = Flask(__name__)

# ========================================================
# ✅ Step 1: Print Environment Variables for Debug
# ========================================================

print("🔧 Environment Variables Loaded:")
env_vars = ["MONGO_URI", "REDSHIFT_HOST", "REDSHIFT_PORT", "REDSHIFT_USER", "REDSHIFT_PASSWORD", "REDSHIFT_DBNAME"]
for var in env_vars:
    print(f"{var}: {os.getenv(var)}")

# ========================================================
# ✅ Step 2: MongoDB Configuration Check
# ========================================================

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ ERROR: MONGO_URI environment variable is not set!")
    sys.exit(1)

try:
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client["MoonInsuranceDB"]
    sales_collection = mongo_db["Sales"]
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ ERROR: Failed to connect to MongoDB: {e}")
    sys.exit(1)

# ========================================================
# ✅ Step 3: Redshift Configuration Check
# ========================================================

REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_PORT = int(os.getenv("REDSHIFT_PORT", 5439))
REDSHIFT_DBNAME = os.getenv("REDSHIFT_DBNAME")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")

# Validate Redshift env vars
redshift_env_vars = [REDSHIFT_HOST, REDSHIFT_DBNAME, REDSHIFT_USER, REDSHIFT_PASSWORD]
if not all(redshift_env_vars):
    print("❌ ERROR: One or more Redshift environment variables are missing!")
    sys.exit(1)

# ========================================================
# ✅ Step 4: Redshift Connection Function
# ========================================================

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
        print(f"❌ ERROR: Redshift connection failed: {e}")
        return None

# ========================================================
# ✅ Step 5: Health Check Endpoint
# ========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Moon Insurance Redshift Analytics Service is running 🚀"}), 200

# ========================================================
# ✅ Step 6: Sync Best Performing Sales Teams
# ========================================================

@app.route('/sync/best_teams', methods=['POST'])
def sync_best_teams():
    try:
        pipeline = [
            {"$group": {"_id": "$team_name", "total_sales": {"$sum": 1}}},
            {"$sort": {"total_sales": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        print(f"🔍 Aggregated Best Teams: {results}")

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
            cursor.execute("""
                INSERT INTO best_teams (team_name, total_sales)
                VALUES (%s, %s)
            """, (result["_id"], result["total_sales"]))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Best teams synced to Redshift ✅", "data": results}), 200

    except Exception as e:
        print(f"❌ ERROR in sync_best_teams: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================================
# ✅ Step 7: Sync Products Achieving Targets
# ========================================================

@app.route('/sync/products_achieving_targets', methods=['POST'])
def sync_products_achieving_targets():
    try:
        target_sales = 10  # Example threshold
        pipeline = [
            {"$group": {"_id": "$product_name", "total_sales": {"$sum": 1}}},
            {"$match": {"total_sales": {"$gte": target_sales}}},
            {"$sort": {"total_sales": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        print(f"🔍 Aggregated Products Achieving Targets: {results}")

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
            cursor.execute("""
                INSERT INTO products_achieving_targets (product_name, total_sales)
                VALUES (%s, %s)
            """, (result["_id"], result["total_sales"]))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Products achieving targets synced to Redshift ✅", "data": results}), 200

    except Exception as e:
        print(f"❌ ERROR in sync_products_achieving_targets: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================================
# ✅ Step 8: Sync Branch Wise Sales Performance
# ========================================================

@app.route('/sync/branch_wise_performance', methods=['POST'])
def sync_branch_wise_performance():
    try:
        pipeline = [
            {"$group": {"_id": "$branch", "total_sales": {"$sum": 1}}},
            {"$sort": {"total_sales": -1}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        print(f"🔍 Aggregated Branch Wise Sales Performance: {results}")

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
            cursor.execute("""
                INSERT INTO branch_wise_sales_performance (branch_name, total_sales)
                VALUES (%s, %s)
            """, (result["_id"], result["total_sales"]))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Branch wise sales performance synced to Redshift ✅", "data": results}), 200

    except Exception as e:
        print(f"❌ ERROR in sync_branch_wise_performance: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================================
# ✅ Step 9: Start Flask App
# ========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
