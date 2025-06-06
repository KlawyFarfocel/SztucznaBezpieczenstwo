from ultralytics import YOLO
import asyncio
from utils.host_related.is_gpu_available import USE_GPU

async def detect_car_color_async(frame, model):
    loop = asyncio.get_running_loop()

    def sync_task():
        device = "0" if USE_GPU() else "cpu"
        if USE_GPU():
            results = model(frame, device=device, half=True, conf=0.85, verbose=False)
        else:
            results = model(frame, device=device, conf=0.85, verbose=False)

        for result in results:
            if result.boxes:
                predicted_class_ids = result.boxes.cls.int().tolist()
                for predicted_class_id in predicted_class_ids:
                    return model.names[predicted_class_id]
        return None

    return await loop.run_in_executor(None, sync_task)
