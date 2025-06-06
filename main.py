import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
import os
import duckdb

from fast_alpr import ALPR
from utils.frame.display_frame import display_frame
from utils.frame.get_current_frame import get_current_frame
from pipeline.frame.process_frame import process_frame 
import onnxruntime as ort

ort.get_available_providers = lambda: ["CUDAExecutionProvider", "CPUExecutionProvider"]

load_dotenv()

main_model = YOLO(os.getenv('MAIN_MODEL_PATH'))
car_brand_model = YOLO(os.getenv("CAR_BRAND_MODEL_PATH"))
car_color_model = YOLO(os.getenv("CAR_COLOR_MODEL_PATH"))
video_path = os.getenv('VIDEO_PATH')
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers= ["CUDAExecutionProvider"],
)


async def process_and_show(update_ui_callback, should_continue=lambda: True):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened() and should_continue():
        ret, frame = cap.read()
        if not ret:
            break

        frame = await process_frame(frame, main_model, car_brand_model, alpr, car_color_model) 

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        update_ui_callback(frame_rgb)

    cap.release()

