import cv2

def display_frame(frame, window_name, window_size):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_size[0], window_size[1])
    cv2.imshow(window_name, frame)