import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
import os

from utils.frame.get_current_frame import get_current_frame
from pipeline.frame.process_frame import process_frame

load_dotenv()

model = YOLO(os.getenv('MAIN_MODEL_PATH'))

video_path = os.getenv('VIDEO_PATH')
cap = cv2.VideoCapture(video_path)
frame_skip = 2

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

def main():
    """Main loop for video processing."""
    while cap.isOpened():
        ret, frame = cap.read()  # Odczytujemy klatkę synchronicznie

        if not ret:
            break

        should_skip_frame = get_current_frame(cap) % frame_skip
        if should_skip_frame != 0:
            continue

        process_frame(frame, model)  # Przetwarzamy ramkę (detekcja + marka)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

cap.release()
cv2.destroyAllWindows()
