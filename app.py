from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('')
db = client['mongo-instance']
collection = db['user-activities']

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to receive GitHub Webhooks
@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    # Initialize the document with default None values
    doc = {
        "request_id": None,
        "author": None,
        "action": None,
        "from_branch": None,
        "to_branch": None,
        "timestamp": None
    }

    # Handle PUSH actions [cite: 5, 7]
    if event_type == 'push':
        doc["request_id"] = data['head_commit']['id'] # [cite: 27]
        doc["author"] = data['pusher']['name']        # [cite: 27]
        doc["action"] = "PUSH"                        # [cite: 27]
        doc["to_branch"] = data['ref'].split('/')[-1] # Extract branch name
        doc["timestamp"] = data['head_commit']['timestamp']

    # Handle PULL REQUEST and MERGE actions [cite: 5, 10, 13]
    elif event_type == 'pull_request':
        doc["request_id"] = str(data['pull_request']['id'])
        doc["author"] = data['pull_request']['user']['login']
        doc["from_branch"] = data['pull_request']['head']['ref']
        doc["to_branch"] = data['pull_request']['base']['ref']
        
        # Check if it is a MERGE action (Brownie Points) [cite: 13]
        if data['pull_request'].get('merged') is True and data['action'] == 'closed':
             doc["action"] = "MERGE"
             doc["timestamp"] = data['pull_request']['merged_at']
        else:
             doc["action"] = "PULL_REQUEST"
             doc["timestamp"] = data['pull_request']['created_at']

    # Insert into MongoDB only if action is valid
    if doc["action"]:
        collection.insert_one(doc)
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "ignored"}), 200

# API for UI Polling [cite: 6]
@app.route('/events', methods=['GET'])
def get_events():
    # Fetch the latest 10 events, sorted by newest first
    events = list(collection.find({}, {'_id': 0}).sort('_id', -1).limit(10))
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000, debug=True)