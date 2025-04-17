from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# MongoDB connection
try:
    # mongo_uri = os.environ.get("MONGO_URI")
    mongo_uri = os.environ.get("MONGO_URI")
    # mongo_uri = "mongodb://rajithawijesinghe74:ohClusterMoonInsuarancermooninsuarance@j7nq4hq.mongodb.net:27017/?retryWrites=true&w=majority&appName=ClusterMoonInsuarance"  # Replace with your MongoDB URI
    if not mongo_uri:
        raise ValueError("Missing MONGO_URI environment variable.")
    client = MongoClient(mongo_uri)
    db = client['MoonInsuranceDB']
    sales_collection = db['Sales']
    logging.info("✅ Connected to MongoDB successfully!")
except Exception as e:
    logging.error(f"❌ MongoDB connection error: {e}")
    raise e

# Configurable sales target
SALES_TARGET = int(os.environ.get("SALES_TARGET", 5))  # Default is 5 if not set

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Moon Insurance Notification Service is running 🚀"}), 200

# Endpoint to check if sales target is met for agent
# @app.route('/notification/check_target/<agent_code>', methods=['GET'])
# def check_sales_target(agent_code):
#     try:
#         count = sales_collection.count_documents({"agent_code": agent_code})
#         if count >= SALES_TARGET:
#             notification_message = f"🎉 Notification: Agent {agent_code} has achieved sales target with {count} sales!"
#             logging.info(notification_message)
#             return jsonify({"message": f"Agent {agent_code} has achieved sales target!", "sales_count": count}), 200
#         else:
#             logging.info(f"Agent {agent_code} has {count} sales. Target not reached yet.")
#             return jsonify({"message": f"Agent {agent_code} has {count} sales. Target not reached yet."}), 200
#     except Exception as e:
#         logging.error(f"❌ Error in check_sales_target: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5003, debug=True)
@app.route('/notification/check_target/<agent_code>', methods=['GET'])
def check_sales_target(agent_code):
    try:
        pipeline = [
            {"$match": {"agent_code": agent_code}},
            {"$group": {"_id": "$agent_code", "total_sales_value": {"$sum": "$sales_value"}}}
        ]
        results = list(sales_collection.aggregate(pipeline))
        total = results[0]["total_sales_value"] if results else 0

        if total >= SALES_TARGET:
            return jsonify({
                "message": f"Agent {agent_code} reached the sales target! 🎯",
                "total_sales_value": total
            }), 200
        else:
            return jsonify({
                "message": f"Agent {agent_code} has not yet met the target.",
                "total_sales_value": total
            }), 200

    except Exception as e:
        logging.error(f"❌ Error in check_sales_target: {e}")
        return jsonify({"error": str(e)}), 500

 # ========================================================
# ✅ Step 9: Start Flask App
# ========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)