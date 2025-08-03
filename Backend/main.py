# main.py
import cv2
import os
import datetime
import uuid
import time
from pymongo import MongoClient
from bson.binary import Binary
from dotenv import load_dotenv

load_dotenv()

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['CCTV_DB']
faces_col = db['faces']

# RTSP stream
cap = cv2.VideoCapture(os.getenv("CCTV_RTSP_URL"))

# Haar cascade XML for face detection
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

SAVE_DIR = "detected_faces"
os.makedirs(SAVE_DIR, exist_ok=True)

saved_faces = []
save_cooldown = 10  # seconds
min_area = 5000  # to avoid tiny faces being stored

frame_count = 0
buffer_faces = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (960, 540))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    current_time = time.time()
    for (x, y, w, h) in faces:
        if w * h < min_area:
            continue

        face_img = frame[y:y+h, x:x+w]

        # Save buffer for best faces
        uid = f"{x}_{y}_{w}_{h}"
        if uid not in buffer_faces:
            buffer_faces[uid] = []

        buffer_faces[uid].append((face_img.copy(), current_time))

        # Keep only last 10 frames per face
        if len(buffer_faces[uid]) > 10:
            buffer_faces[uid] = buffer_faces[uid][-10:]

    # Every 5 seconds, extract 3 clear frames per face and save
    if frame_count % 150 == 0:
        for uid, images in buffer_faces.items():
            # Pick 3 middle frames as "clearest"
            selected_frames = images[len(images)//2 - 1:len(images)//2 + 2]

            for face_img, ts in selected_frames:
                ts = datetime.datetime.now()
                filename = f"{uuid.uuid4()}.jpg"
                filepath = os.path.join(SAVE_DIR, filename)
                cv2.imwrite(filepath, face_img)

                with open(filepath, "rb") as f:
                    img_data = f.read()

                faces_col.insert_one({
                    "image": Binary(img_data),
                    "filename": filename,
                    "timestamp": ts
                })

        buffer_faces = {}  # clear buffer after saving

    # Draw rectangle around face
    for (x, y, w, h) in faces:
        if w * h < min_area:
            continue
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Capture", frame)
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
