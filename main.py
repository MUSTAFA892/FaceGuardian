import cv2

url = "rtsp://admin:ZWTMVH@192.168.29.7:554/"
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
