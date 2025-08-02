from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
import base64
import pickle
from datetime import datetime
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your-secret-key'  # Required for flash messages

# MongoDB Setup
MONGO_URI = "mongodb+srv://mustafatinwala6:mustafa5253TINWALA@learningmongo.lof7x.mongodb.net/?retryWrites=true&w=majority&appName=LearningMongo"
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['CCTV_DB']
    faces_col = db['faces']
    encodings_col = db['known_encodings']
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    exit(1)

@app.route('/')
def index():
    try:
        faces = []
        for doc in faces_col.find().sort("timestamp", -1):
            faces.append({
                "id": str(doc['_id']),
                "filename": doc['filename'],
                "image": base64.b64encode(doc['image']).decode('utf-8'),
                "name": doc.get("name", "Unknown"),
                "timestamp": doc['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            })
        return render_template('index.html', faces=faces)
    except PyMongoError as e:
        logger.error(f"Failed to fetch faces: {e}")
        flash("Failed to load faces from database", "error")
        return render_template('index.html', faces=[])

@app.route('/rename', methods=['POST'])
def rename():
    try:
        face_id = request.form.get('id')
        new_name = request.form.get('name').strip()

        if not face_id or not new_name:
            flash("Missing ID or name", "error")
            return redirect(url_for('index'))

        try:
            obj_id = ObjectId(face_id)
        except:
            flash("Invalid ID", "error")
            return redirect(url_for('index'))

        face_doc = faces_col.find_one({'_id': obj_id})
        if not face_doc:
            flash("Face not found", "error")
            return redirect(url_for('index'))

        # Update name in faces collection
        faces_col.update_many({'name': face_doc['name']}, {'$set': {'name': new_name}})
        
        # Update or insert encoding in known_encodings
        existing_encoding = encodings_col.find_one({'name': face_doc['name']})
        if existing_encoding:
            encodings_col.update_one({'name': face_doc['name']}, {'$set': {'name': new_name}})
        else:
            encoding = pickle.loads(face_doc["encoding"])
            encodings_col.insert_one({
                'name': new_name,
                'encoding': Binary(pickle.dumps(encoding)),
                'created_at': datetime.now()
            })

        flash("Name updated successfully", "success")
        return redirect(url_for('index'))
    except PyMongoError as e:
        logger.error(f"Failed to rename face: {e}")
        flash("Failed to rename face", "error")
        return redirect(url_for('index'))

# Kept for potential API use
@app.route('/api/faces', methods=['GET'])
def get_faces():
    try:
        faces = []
        for doc in faces_col.find().sort("timestamp", -1):
            faces.append({
                "id": str(doc['_id']),
                "filename": doc['filename'],
                "image": base64.b64encode(doc['image']).decode('utf-8'),
                "name": doc.get("name", "Unknown"),
                "timestamp": doc['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            })
        return jsonify(faces)
    except PyMongoError as e:
        logger.error(f"Failed to fetch faces: {e}")
        return jsonify({"error": "Failed to fetch faces"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)