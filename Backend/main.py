import cv2
import os
import datetime
import uuid
from deepface import DeepFace
from pymongo import MongoClient
from pymongo.errors import ConnectionError, PyMongoError
from bson.binary import Binary
import pickle
import numpy as np
import time
import logging
import signal
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB Setup
MONGO_URI = "mongodb+srv://mustafatinwala6:mustafa5253TINWALA@learningmongo.lof7x.mongodb.net/?retryWrites=true&w=majority&appName=LearningMongo"
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test connection
    db = client['CCTV_DB']
    faces_col = db['faces']
    encodings_col = db['known_encodings']
    logger.info("Connected to MongoDB")
except ConnectionError as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    sys.exit(1)

# Video Capture Setup
cap = cv2.VideoCapture("rtsp://admin:ZWTMVH@192.168.29.7:554/")
if not cap.isOpened():
    logger.error("Failed to open RTSP stream")
    sys.exit(1)

# Create directory for saving faces
SAVE_DIR = "detected_faces"
os.makedirs(SAVE_DIR, exist_ok=True)

# Load known encodings
known_encodings = []
known_names = []
try:
    for doc in encodings_col.find():
        known_encodings.append(pickle.loads(doc["encoding"]))
        known_names.append(doc["name"])
    logger.info(f"Loaded {len(known_encodings)} known encodings")
except PyMongoError as e:
    logger.error(f"Failed to load encodings: {e}")

# Unknown face tracking
unknown_encodings = []
unknown_labels = []
person_counter = 1

def variance_of_laplacian(img):
    """Calculate image sharpness using Laplacian variance"""
    return cv2.Laplacian(img, cv2.CV_64F).var()

def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    logger.info("Shutting down...")
    cap.release()
    cv2.destroyAllWindows()
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            logger.warning("Failed to capture frame")
            time.sleep(1)
            continue

        frame = cv2.resize(frame, (960, 540))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces using DeepFace
        try:
            faces = DeepFace.extract_faces(rgb_frame, detector_backend='retinaface', enforce_detection=False)
        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            continue

        for face in faces:
            if face['confidence'] < 0.9:  # Filter low-confidence faces
                continue

            facial_area = face['facial_area']
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            top, right, bottom, left = y, x + w, y + h, x

            # Extract face embedding
            try:
                embedding = DeepFace.represent(rgb_frame[top:bottom, left:right], model_name='Facenet', enforce_detection=True)[0]["embedding"]
            except Exception as e:
                logger.warning(f"Failed to compute embedding: {e}")
                continue

            name = "Unknown"
            label = "Unknown Face"

            # Compare with known encodings
            if known_encodings:
                distances = [np.linalg.norm(np.array(embedding) - np.array(ke)) for ke in known_encodings]
                min_distance = min(distances)
                if min_distance < 0.5:  # Threshold for match
                    best_match_index = distances.index(min_distance)
                    name = known_names[best_match_index]
                    label = f"Recognized: {name}"
                else:
                    # Check unknown faces
                    distances_unknown = [np.linalg.norm(np.array(embedding) - np.array(ue)) for ue in unknown_encodings]
                    if distances_unknown and min(distances_unknown) < 0.5:
                        idx = distances_unknown.index(min(distances_unknown))
                        name = unknown_labels[idx]
                        label = f"Recognized: {name}"
                    else:
                        # New unknown face
                        name = f"Person_{person_counter}"
                        person_counter += 1
                        unknown_encodings.append(embedding)
                        unknown_labels.append(name)
                        label = f"New Face: {name}"

                        # Capture high-quality face images
                        buffered_faces = []
                        logger.info(f"Capturing 5 frames for {name}...")
                        for _ in range(10):
                            ret2, buffer_frame = cap.read()
                            if not ret2:
                                continue
                            buffer_frame = cv2.resize(buffer_frame, (960, 540))
                            buffer_rgb = cv2.cvtColor(buffer_frame, cv2.COLOR_BGR2RGB)
                            try:
                                buffer_faces = DeepFace.extract_faces(buffer_rgb, detector_backend='retinaface', enforce_detection=False)
                                for bf in buffer_faces:
                                    if bf['confidence'] >= 0.9:
                                        bf_area = bf['facial_area']
                                        face_img = buffer_frame[bf_area['y']:bf_area['y']+bf_area['h'], bf_area['x']:bf_area['x']+bf_area['w']]
                                        buffered_faces.append((face_img, variance_of_laplacian(face_img)))
                            except Exception as e:
                                logger.warning(f"Buffer frame processing failed: {e}")
                            time.sleep(0.05)

                        # Save top 5 sharpest images
                        buffered_faces.sort(key=lambda x: x[1], reverse=True)
                        top_images = buffered_faces[:5]
                        for img, _ in top_images:
                            uid = str(uuid.uuid4())
                            timestamp = datetime.datetime.now()
                            filename = f"{name}_{uid}.jpg"
                            filepath = os.path.join(SAVE_DIR, filename)
                            cv2.imwrite(filepath, img)
                            with open(filepath, "rb") as f:
                                img_data = f.read()
                            try:
                                faces_col.insert_one({
                                    "image": Binary(img_data),
                                    "filename": filename,
                                    "timestamp": timestamp,
                                    "name": name,
                                    "encoding": Binary(pickle.dumps(embedding))
                                })
                            except PyMongoError as e:
                                logger.error(f"Failed to save face to MongoDB: {e}")

            # Draw rectangle and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        time.sleep(1)

cap.release()
cv2.destroyAllWindows()
client.close()
logger.info("Application terminated")