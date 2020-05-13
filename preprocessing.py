import cv2


def preprocess(img):
    # add edge detection
    edges = cv2.Canny(img, 100, 200)
    img = edges

    return img