import asyncio
import cv2
import threading
from utils.host_related.is_gpu_available import USE_GPU
from utils.frame.display_frame import display_frame
from pipeline.car_feature_extraction.car_brand.car_brand import detect_car_brand
from utils.extract_box import extract_car

# Słownik przechowujący przypisane marki do track_id samochodów
car_brands = {}
lock = threading.Lock()  # Mutex do synchronizacji dostępu do car_brands

frame_counter = 0  # Licznik klatek

def process_frame(frame, model):
    """Przetwarzanie pojedynczej klatki - wykrywanie samochodów synchronicznie,
       a marek asynchronicznie co 5 klatek."""

    global frame_counter
    frame_counter += 1

    if USE_GPU():
        results = model.track(frame, device='0', classes=[2], half=True, persist=True, conf=0.75, verbose=False)
    else:
        results = model.track(frame, device="cpu", classes=[2], persist=True, conf=0.75, verbose=False)

    for result in results:
        draw_custom_annotations(frame, result)

        for i, cropped_box in enumerate(extract_car(frame, result, "car")):
            track_id = result.boxes.id[i].item() if result.boxes.id is not None else None
            if track_id:
                # Aktualizujemy markę co 5 klatek
                if frame_counter == 0 or frame_counter % 5 == 0:
                    threading.Thread(target=handle_car_brand_detection, args=(track_id, cropped_box)).start()

    display_frame(frame, "Detected frame", (1280, 720))


def handle_car_brand_detection(track_id, cropped_box):
    """Obsługuje wykrywanie marki w osobnym wątku."""
    car_brand = asyncio.run(detect_car_brand(cropped_box))
    if car_brand:
        with lock:
            car_brands[track_id] = car_brand


def draw_custom_annotations(frame, result):
    """Rysowanie bounding boxów oraz wyświetlanie marki."""
    for i, box in enumerate(result.boxes.xyxy):
        track_id = result.boxes.id[i].item() if result.boxes.id is not None else None
        if track_id:
            x1, y1, x2, y2 = map(int, box)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            with lock:
                brand_text = f"ID:{int(track_id)}"
                if track_id in car_brands:
                    brand_text += f" Marka: {car_brands[track_id]}"

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 4
            text_color = (255, 255, 255)
            outline_color = (0, 0, 0)

            (text_width, text_height), baseline = cv2.getTextSize(brand_text, font, font_scale, font_thickness)

            text_x, text_y = x1, max(y1 - 15, 30)

            for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
                cv2.putText(frame, brand_text, (text_x + dx, text_y + dy), font, font_scale, outline_color,
                            font_thickness)

            cv2.putText(frame, brand_text, (text_x, text_y), font, font_scale, text_color, font_thickness)
