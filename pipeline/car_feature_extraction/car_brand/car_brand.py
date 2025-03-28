from ultralytics import YOLO
import os
import cv2

def detect_car_brand(frame):
    model = YOLO(os.getenv('CAR_BRAND_MODEL_PATH'))
    resized_frame = cv2.resize(frame, (800, 600))
    results = model(resized_frame, imgsz=(800,600))
    for result in results:
        annotated_frame = result.plot()

        cv2.imshow("Chleb", annotated_frame)
        cv2.waitKey(0)
        cv2.destroyWindow("Chleb")