from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId
import base64
import os
import pickle
from datetime import datetime
from collections import defaultdict
import calendar
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['CCTV_DB']
collection = db['faces']
encodings_col = db['encodings']

# Helper to group faces and calculate statistics
def group_faces_by_date():
    grouped = defaultdict(list)
    total_faces = 0
    identified_faces = 0
    
    for doc in collection.find().sort("timestamp", -1):
        date_str = doc["timestamp"].strftime("%A, %d %B %Y")
        image_base64 = base64.b64encode(doc['image']).decode('utf-8')
        
        face_data = {
            "id": str(doc['_id']),
            "filename": doc['filename'],
            "image": image_base64,
            "name": doc.get("name", ""),
            "timestamp": doc['timestamp'].strftime("%I:%M %p")
        }
        
        grouped[date_str].append(face_data)
        total_faces += 1
        
        # Count identified faces (those with names)
        if doc.get("name") and doc.get("name").strip():
            identified_faces += 1
    
    # Calculate statistics
    stats = {
        'total_faces': total_faces,
        'identified_faces': identified_faces,
        'total_days': len(grouped)
    }
    
    return grouped, stats

@app.route('/')
def index():
    grouped_faces, stats = group_faces_by_date()
    return render_template("index.html", grouped_faces=grouped_faces, stats=stats)

@app.route('/delete', methods=['POST'])
def delete_faces():
    ids = request.form.getlist('selected_faces')
    for face_id in ids:
        collection.delete_one({'_id': ObjectId(face_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)