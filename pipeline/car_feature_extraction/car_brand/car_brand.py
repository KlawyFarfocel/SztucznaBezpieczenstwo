from ultralytics import YOLO
import os
import asyncio
from dotenv import load_dotenv

from utils.host_related.is_gpu_available import USE_GPU

load_dotenv()
model = YOLO(os.getenv("CAR_BRAND_MODEL_PATH"))


async def detect_car_brand(frame):
    """Rozpoznawanie marki samochodu - wersja asynchroniczna."""

    loop = asyncio.get_running_loop()

    def sync_task():
        if USE_GPU():
            results = model(frame, device="0", half=True, conf=0.6, verbose=False)
        else:
            results = model(frame, device="cpu", conf=0.6, verbose=False)

        for result in results:
            if result.boxes:
                predicted_class_ids = result.boxes.cls.int().tolist()
                for predicted_class_id in predicted_class_ids:
                    return model.names[predicted_class_id]
        return None

    return await loop.run_in_executor(None, sync_task)  # Uruchamiamy YOLO w tle
