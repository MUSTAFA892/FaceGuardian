📹 **CCTV Face Recognition System using RTSP, OpenCV, DeepFace, and Flask**

This project enables real-time face detection and recognition from an RTSP-enabled IP camera feed using Python + OpenCV + DeepFace. It stores detected faces and their encodings in MongoDB Atlas and provides a responsive Flask-based web interface for viewing and renaming faces. The system is configured to work on a JioFiber network, with support for local access and optional port forwarding for remote access.

🔧 **Features**

* 📡 **Live RTSP Streaming:** Access live camera feed via RTSP protocol.
* 🧠 **Face Detection & Recognition:** Uses DeepFace (RetinaFace backend) for accurate face detection and recognition, reducing false positives (e.g., clothes misidentified as faces).
* 💾 **MongoDB Storage:** Stores face images, encodings, and metadata (name, timestamp) in MongoDB Atlas.
* 🌐 **Responsive Web Interface:** Flask-based frontend with Bootstrap 5 for viewing faces, renaming them, and displaying success/error messages.
* 🔄 **Auto-Refresh:** Web interface refreshes every 5 seconds to display new faces.
* 📶 **JioFiber Network Setup:** Instructions for local network access and port forwarding for remote viewing.
* 🛠️ **Robust Error Handling:** Comprehensive logging and user feedback for camera, database, and processing errors.
* 🖼️ **Image Quality Filtering:** Selects sharp, high-confidence face images for storage.

🧠 **Project Overview**

This repo guides you through:

* Accessing the RTSP feed from an IP camera in the local network.
* Performing real-time face detection and recognition using DeepFace and OpenCV.
* Storing and managing face data in MongoDB Atlas.
* Serving a Flask web interface to view and rename detected faces.
* Configuring JioFiber router port forwarding for remote access.
* Troubleshooting common issues with RTSP, MongoDB, and network setup.

🖥️ **Face Recognition System**
The system consists of two main components:

* **Backend (main.py):** Captures the RTSP feed, detects and recognizes faces using DeepFace, and stores face images and encodings in MongoDB Atlas.
* **Frontend (app.py):** Serves a Flask-based web interface to display detected faces, allowing users to rename them with persistent updates to the database.

🏠 **Local Network Setup**

1. Find your camera’s local IP address (e.g., 192.168.29.7).
2. Verify the RTSP port, usually 554, sometimes 8000, via the camera's LAN settings.
3. Test the camera feed using VLC or the provided Python script on the same local network.

🌐 **JioFiber Router - Port Forwarding**

1. **Accessing JioFiber Dashboard:**

   * Go to: [http://192.168.29.1](http://192.168.29.1)
   * Login:

     * Username: admin
     * Password: Jiocentrum (default, if not changed)
2. **Add Port Forwarding:**

   * Navigate to Applications → Port Forwarding.
   * Add a new rule:

     * Name: RTSP
     * Protocol: TCP
     * Port: 554 or 8000 (match your camera setting)
     * Internal IP: Your camera’s IP (192.168.29.7)
   * Save and reboot router if necessary.

🌐 **Understanding IPs and Routing**

| Type         | Example      | Description                                               |
| ------------ | ------------ | --------------------------------------------------------- |
| 📍 Local IP  | 192.168.29.7 | IP given to your camera by the router (internal use only) |
| 🌎 Public IP | 49.xx.xx.xx  | Your JioFiber connection’s external IP (seen on internet) |
| 📦 Router    | 192.168.29.1 | Gateway that manages traffic between local and internet   |

**How It Connects**

* Your router assigns local IPs to devices (camera, laptop).
* The camera exposes an RTSP feed at a port (e.g., 554).
* The backend script accesses it via the local IP.
* For external access, port forwarding maps public IP traffic to the camera.

💿 **Setup Instructions**

**Prerequisites**

* Python 3.8+
* MongoDB Atlas account with a cluster (URI provided in code)
* RTSP-enabled IP camera (e.g., with URL rtsp\://admin\:ZWTMVH\@192.168.29.7:554/)
* JioFiber router for network configuration

**Directory Structure**

```
project/
├── main.py              # Video processing and face detection
├── app.py               # Flask API and frontend
├── templates/
│   └── index.html      # Frontend template with Bootstrap
├── static/
│   └── styles.css      # Custom CSS for styling
├── detected_faces/      # Directory for saving face images
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

**Installation**

1. Clone the repository:

   ```
   git clone <repository-url>
   cd project
   ```
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

**Contents of `requirements.txt`:**

* opencv-python
* deepface
* pymongo
* flask
* numpy

3. Ensure MongoDB Atlas is configured with the provided URI.
4. Verify the RTSP URL in `main.py` matches your camera's settings.

**Running the Application**

1. Start the backend for face detection and storage:

   ```
   python main.py
   ```
2. Start the Flask web server for the frontend:

   ```
   python app.py
   ```
3. Access the web interface at [http://localhost:5000](http://localhost:5000).

💡 **Notes & Debugging Tips**

* **RTSP Issues:** Test the RTSP feed with VLC (Media → Open Network Stream). Try alternate ports (554 or 8000) if the feed fails. Ensure the camera IP and credentials are correct.
* **MongoDB Issues:** Verify the MongoDB Atlas URI and network access (whitelist your IP). Check for connection errors in logs.
* **Web Interface:** The interface auto-refreshes every 5 seconds. Adjust the interval in `index.html` if needed. Ensure names are 1-50 characters for renaming.
* **Port Forwarding:** Restart the router and camera after changing configurations. If port 554 is blocked, try an alternate port and update the camera settings.

📌 **Final Checklist**

* ✅ Confirm camera IP and RTSP port (554 or 8000)
* ✅ Validate RTSP feed in local network using VLC
* ✅ Set up MongoDB Atlas with correct URI
* ✅ Install dependencies and run `main.py` and `app.py`
* ✅ Configure JioFiber port forwarding for remote access (if needed)
* ✅ Keep JioFiber dashboard login handy (admin / Jiocentrum)

🧾 **Credits & Author**
Maintained by Mustafa Tinwala
Built for personal learning and CCTV face recognition experiments using open technologies.

📎 **License**
MIT License - free to use, modify, and share.