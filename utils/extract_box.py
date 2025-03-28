import cv2


def extract_car(frame, result, className):
    car_class_id = list(result.names.keys())[list(result.names.values()).index(className)]

    for i, box in enumerate(result.boxes):
        class_id = int(box.cls[0])


        if class_id == car_class_id:
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            cropped_box = frame[int(y1):int(y2), int(x1):int(x2)]
            yield cropped_box
