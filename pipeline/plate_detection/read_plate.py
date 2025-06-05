from fast_alpr import ALPR
import cv2

def read_plate(frame):

    cv2.imshow("Rama", frame)

    key = cv2.waitKey(0)
    cv2.destroyWindow('Rama')

    if key == ord('q'):
        print("Exiting...")

