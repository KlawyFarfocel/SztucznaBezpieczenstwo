import cv2

def get_current_frame(cap):
    return int(cap.get(cv2.CAP_PROP_POS_FRAMES))