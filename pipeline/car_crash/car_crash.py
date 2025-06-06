import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('data/models/cantbeworse.pt')
cap = cv2.VideoCapture('data/videos/carcrash3.mp4')

last_positions = {}

def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
     ret, frame = cap.read()
     if not ret:
        print("Nie udało się odczytać klatki.")
        break

     results = model(frame, device='0', half=True, conf=0.45, verbose=False)

     annotated_frame = results[0].plot()

     cv2.imshow("YOLO Detekcja", annotated_frame)

     if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnij zasoby
cap.release()
cv2.destroyAllWindows()