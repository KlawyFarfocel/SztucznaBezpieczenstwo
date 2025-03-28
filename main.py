import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
from utils.extract_box import extract_car
from pipeline.plate_detection.read_plate import read_plate
from pipeline.car_feature_extraction.car_brand.car_brand import detect_car_brand
import os
import random

load_dotenv()

model = YOLO(os.getenv('MAIN_MODEL_PATH'))

video_path = os.getenv('VIDEO_PATH')
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    if os.getenv('USE_GPU'):
        results = model(frame, device=0, classes=[2])
    else:
        results = model(frame)


    for result in results:
        annotated_frame = result.plot()

        for i, cropped_box in enumerate(extract_car(frame, result, "car")):
            detect_car_brand(cropped_box)

        cv2.namedWindow("YOLO Detection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("YOLO Detection",1280,720)
        cv2.imshow("YOLO Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
