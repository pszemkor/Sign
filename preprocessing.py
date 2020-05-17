import cv2

# def preprocess(img):
#     # add edge detection
#     edges = cv2.Canny(img, 100, 200)
#     img = edges
#
#     return img


def preprocess(cam, h, hist, w, x, y):
    img, imgHSV = process_img(cam)
    dst = cv2.calcBackProject([imgHSV], [0, 1], hist, [0, 180, 0, 256], 1)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    cv2.filter2D(dst, -1, disc, dst)
    blur = cv2.GaussianBlur(dst, (11, 11), 0)
    blur = cv2.medianBlur(blur, 15)
    thresh = prepare_thresh(blur, h, w, x, y)
    return img, thresh


def process_img(cam):
    img = cam.read()[1]
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (640, 480))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img, imgHSV


def prepare_thresh(blur, h, w, x, y):
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    thresh = cv2.merge((thresh, thresh, thresh))
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    thresh = thresh[y:y + h, x:x + w]
    return thresh
