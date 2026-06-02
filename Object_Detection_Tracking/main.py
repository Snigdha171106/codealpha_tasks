import cv2
from ultralytics import YOLO

# More accurate than yolov8n
model = YOLO("yolov8s.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detection + Tracking
    results = model.track(
        frame,
        persist=True,
        conf=0.5,      # ignore weak detections
        verbose=False
    )

    annotated_frame = results[0].plot()

    cv2.imshow(
        "Object Detection and Tracking",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()