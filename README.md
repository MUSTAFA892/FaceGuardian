# 🎩 CCTV Face Recognition System using RTSP, OpenCV, DeepFace, and Flask

This project enables real-time face detection from an RTSP-enabled IP camera feed using Python, OpenCV, and DeepFace. It stores detected face snapshots in MongoDB Atlas and provides a responsive Flask-based web interface for browsing them. Designed to run on a JioFiber home network with optional port forwarding.

---

## 🔧 Features

- 📱 **Live RTSP Feed Access**: Captures real-time video from an IP camera over RTSP.
- 🧠 **Accurate Face Detection (DeepFace)**: RetinaFace model ensures high-accuracy face localization and avoids false positives.
- 📅 **Smart Storage to MongoDB**: Stores only 3–4 clear frames per face with timestamps.
- 🌐 **Responsive Flask Web UI**:
  - View detected faces sorted by **day, time, and week**.
  - **Select / Deselect all** and **bulk delete** faces.
  - Auto-refresh every 5 seconds.
- 📀 **Image Quality Filtering**: Only clear, front-facing frames are selected for storage.
- 📅 **Timestamped Faces**: Sorted by detection time, helpful for tracking.
- 🌎 **JioFiber-Compatible Setup**: With instructions for RTSP access and router configuration.

---

## 🧠 System Architecture

**Backend:** `main.py`
- Captures frames via OpenCV from RTSP stream
- Uses `DeepFace` (RetinaFace) for face detection
- Stores selected face images in MongoDB Atlas (3-4 clearest frames per detection)

**Frontend:** `app.py`
- Flask server displays detected faces
- Allows deletion (single/bulk)
- Sorts faces by date, week, and time

---

## 🏠 Local Network Setup

1. **Find camera IP** (e.g., `192.168.29.7`) in router settings
2. Use an RTSP-compatible camera and ensure it's broadcasting (usually port 554)
3. Test with VLC: `rtsp://admin:yourpassword@192.168.29.7:554`

---

## 🚀 JioFiber Port Forwarding (Optional)

1. Login to [http://192.168.29.1](http://192.168.29.1)
   - Username: `admin`
   - Password: `Jiocentrum` (default)

2. Go to `Applications > Port Forwarding`
3. Create rule:
   - Protocol: TCP
   - External & Internal Port: `554` or your RTSP port
   - Internal IP: your camera's IP (e.g., `192.168.29.7`)

---

## 🔹 IP Address Types

| Type         | Example      | Purpose                                   |
|--------------|--------------|-------------------------------------------|
| Local IP     | 192.168.29.7 | Internal network use                      |
| Router IP    | 192.168.29.1 | Gateway to internet                       |
| Public IP    | 49.xx.xx.xx  | Used for remote access (if port forwarded)|

---

## 🔹 Directory Structure

```
project/
├── main.py              # Real-time video processing and face capture
├── app.py               # Flask frontend server
├── templates/
│   └── index.html       # Web UI with Bootstrap 5 and JS
├── static/
│   └── styles.css       # Optional: custom styles
├── detected_faces/      # Optional: saved image backup
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🎓 Prerequisites

- Python 3.8+
- MongoDB Atlas account (free cluster is fine)
- IP camera with RTSP enabled
- JioFiber router (optional for port forwarding)

---

## 🔧 Installation & Setup

1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd project
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set MongoDB URI in both `main.py` and `app.py`
4. Verify your camera RTSP URL in `main.py`

---

## 🚪 Running the Application

1. **Start the video processor** (captures faces):
   ```bash
   python main.py
   ```
2. **Start the Flask server** (to view faces):
   ```bash
   python app.py
   ```
3. Open your browser at [http://localhost:5000](http://localhost:5000)

---

## 📆 Features on the Web Interface

- Live updates (every 5s)
- Day, week, and date grouping
- Image previews with timestamp
- Select individual or all images
- Bulk delete selected images

---

## 📓 requirements.txt

```
Flask==2.3.3
opencv-python==4.9.0.80
deepface==0.40.1
pymongo==4.6.1
numpy==1.26.4
```

---

## 🔎 Debugging Tips

- **RTSP Not Working?**
  - Use VLC to verify stream
  - Check credentials and IP
- **No Faces Detected?**
  - Make sure lighting is good and camera is working
  - Try printing DeepFace output confidence scores
- **MongoDB Issues?**
  - Make sure IP is whitelisted
  - Double-check Mongo URI

---

## 👤 Author
**Mustafa Tinwala**
- GitHub: [@mustafatinwala](https://github.com/mustafatinwala)

---

## 📚 License
MIT License — Free to use, modify, and share.
