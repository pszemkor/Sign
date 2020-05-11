import cv2

def get_video():
    cam = cv2.VideoCapture(0)

    while (True):
        ret, frame = cam.read()
        img = cv2.flip(frame, 1)

        cv2.imshow('frame', img)
        key = cv2.waitKey(1)
        # 27 - ESC key
        if key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

get_video()