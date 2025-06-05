import asyncio
import cv2
import os
import duckdb
import uuid
from utils.host_related.is_gpu_available import USE_GPU
from utils.frame.display_frame import display_frame
from pipeline.car_feature_extraction.car_brand.car_brand import detect_car_brand_async 
from pipeline.car_feature_extraction.car_color.car_color import detect_car_color_async
from utils.extract_box import extract_car

processed_track_ids = set()
car_brands = {}
car_registration_numbers = {}
car_colors = {}
last_processed_frame = {}
db_path = os.getenv("DATABASE_PATH1")
frame_counter = 0

async def process_frame(frame, main_model, car_brand_model, alpr):
    global frame_counter
    frame_counter += 1

    device = '0' if USE_GPU() else 'cpu'
    results = await run_in_executor(main_model.track, frame, device=device, classes=[2], persist=True, conf=0.75, verbose=False)

    for result in results:
        draw_custom_annotations(frame, result)

        for i, cropped_box in enumerate(extract_car(frame, result, "car")):
            track_id = result.boxes.id[i].item() if result.boxes.id is not None else None
            if not track_id:
                continue

            last_frame = last_processed_frame.get(track_id, -5)

            if frame_counter - last_frame >= 10:
                last_processed_frame[track_id] = frame_counter

                car_plate = alpr.predict(cropped_box)
                if car_plate:
                    new_conf = car_plate[0].ocr.confidence
                    if new_conf > 0.94:
                        existing = car_registration_numbers.get(track_id)
                        if not existing or existing["confidence"] < new_conf:
                            car_registration_numbers[track_id] = {
                                "text": car_plate[0].ocr.text,
                                "confidence": new_conf
                            }

                if track_id not in processed_track_ids:
                    car_brand = await detect_car_brand_async(cropped_box, car_brand_model)
                    car_color = await detect_car_color_async(cropped_box)

                    if car_brand:
                        car_brands[track_id] = car_brand
                        processed_track_ids.add(track_id)
                    if car_color:
                        car_colors[track_id] = car_color

                        # TODO zapisz w bazie - wypierdol vechicle_type
                    #     conn = duckdb.connect(db_path)
                    #     new_id = str(uuid.uuid4())
                    #     conn.execute("""
                    #     INSERT INTO vehicles (id, license_plate, vehicle_type, vehicle_brand, color)
                    #     VALUES (?, ?, ?, ?, ?)
                    # """, (new_id, 'PLACEHOLDER_PLATE', 'KOMBI_PLACEHOLDER', car_brand, 'PLACEHOLDER_COLOR'))
                    # # Zamknięcie połączenia
                    #     conn.close()
    return frame
    


def draw_custom_annotations(frame, result):
    for i, box in enumerate(result.boxes.xyxy):
        track_id = result.boxes.id[i].item() if result.boxes.id is not None else None
        if not track_id:
            continue

        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        brand_text = f"ID:{int(track_id)}"
        if track_id in car_brands:
            brand_text += f" Marka: {car_brands[track_id]}"
        if track_id in car_registration_numbers:
            brand_text += f" Rejestracja: {car_registration_numbers[track_id]['text']}"
        if track_id in car_colors:
            brand_text += f" Kolor: {car_colors[track_id]}"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 4
        text_color = (255, 255, 255)
        outline_color = (0, 0, 0)

        (text_width, text_height), baseline = cv2.getTextSize(brand_text, font, font_scale, font_thickness)
        text_x, text_y = x1, max(y1 - 15, 30)

        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
            cv2.putText(frame, brand_text, (text_x + dx, text_y + dy), font, font_scale, outline_color, font_thickness)

        cv2.putText(frame, brand_text, (text_x, text_y), font, font_scale, text_color, font_thickness)


async def run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
