# 📹 CCTV Feed Viewer using RTSP, OpenCV, and JioFiber Network

This project allows you to **stream live CCTV footage** from an RTSP-enabled IP camera (like a DVR or NVR setup) using **Python + OpenCV**. It also explains **how to configure local network access** and optionally **use port forwarding via JioFiber router** for remote access.

---

## 🔧 Features

- 📡 Access live camera stream via RTSP
- 🧠 Understand internal (private) and external (public) IPs
- 📶 JioFiber router dashboard setup for port forwarding
- 🧪 Validate camera feed locally before public setup
- 🧾 Step-by-step configuration and Python integration

---

## 🧠 Project Overview

This repo walks you through:

1. Accessing the **RTSP feed** from your camera in the local network.
2. Viewing the camera stream using **OpenCV** in Python.
3. Understanding and using **local (private) IPs** and **public IPs**.
4. Configuring **JioFiber router port forwarding** to enable remote viewing.
5. Troubleshooting and notes on real-world edge cases.

---

## 🖥️ RTSP Feed Testing with Python

### ✅ Code (Tested Working)

```python
import cv2

# Replace with your actual RTSP URL
url = "rtsp://admin:ZWTMVH@192.168.29.7:554/h264"
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
````

---

## 🏠 Local Network Setup

* Find your camera’s **local IP address** (e.g., `192.168.29.7`).
* Verify the **RTSP port**, usually `554`, sometimes `8000`, via camera's LAN settings.
* Test the camera feed using VLC or Python OpenCV on the same local network.

---

## 🌐 JioFiber Router - Port Forwarding

### Accessing JioFiber Dashboard

* Go to: `http://192.168.29.1`
* Login:

  * Username: `admin`
  * Password: `Jiocentrum` *(default, if not changed)*

> Forgot your WiFi password? Log in above and check under **Wireless Settings → Security**.

---

### Add Port Forwarding

* Navigate to **Applications → Port Forwarding**.
* Add a new rule:

  * **Name**: `RTSP`
  * **Protocol**: `TCP`
  * **Port**: `554` or `8000` *(match your camera setting)*
  * **Internal IP**: Your camera’s IP (`192.168.29.7`)
* Save and reboot router if necessary.

---

## 🌐 Understanding IPs and Routing

| Type         | Example        | Description                                               |
| ------------ | -------------- | --------------------------------------------------------- |
| 📍 Local IP  | `192.168.29.7` | IP given to your camera by the router (internal use only) |
| 🌎 Public IP | `49.xx.xx.xx`  | Your JioFiber connection’s external IP (seen on internet) |
| 📦 Router    | `192.168.29.1` | Gateway that manages traffic between local and internet   |

### How It Connects

1. Your **router assigns local IPs** to devices (camera, laptop).
2. The camera exposes an RTSP feed at a port (e.g., 554).
3. **OpenCV** or **VLC** accesses it via that local IP.
4. For **external access**, port forwarding maps public IP traffic → camera.

---

## 💡 Notes & Debugging Tips

* If RTSP doesn’t work:

  * Test with `VLC → Media → Open Network Stream`
  * Try port `8000` or `554`
* If router doesn’t allow port `554`, try alternate ports and update camera settings
* Restart both router and camera after changing configs

---

## 📌 Final Checklist

✅ Confirm camera IP
✅ Confirm RTSP port (554/8000)
✅ Validate in local network using OpenCV
✅ Configure JioFiber port forwarding if remote access is needed
✅ Keep JioFiber dashboard login handy (`admin / Jiocentrum`)

---

## 🧾 Credits & Author

Maintained by **\[Your Name]**
Built for **personal learning and remote CCTV access experiments** using open technologies.

---

## 📎 License

MIT License - free to use, modify, and share.
