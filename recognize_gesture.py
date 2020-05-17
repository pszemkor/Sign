import cv2, pickle
import numpy as np
import sqlite3
from keras.models import load_model

from preprocessing import preprocess

prediction = None
model = load_model('cnn_model_keras2.h5')


def get_image_size():
    img = cv2.imread('gestures/0/100.jpg', 0)
    return img.shape


image_x, image_y = get_image_size()


def tf_process_image(img):
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    np_array = np.array(img)
    return np_array


def keras_process_image(img):
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, image_x, image_y, 1))
    return img


def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def get_pred_text_from_db(pred_class):
    conn = sqlite3.connect("gesture_db.db")
    cmd = "SELECT g_name FROM gesture WHERE g_id=" + str(pred_class)
    cursor = conn.execute(cmd)
    for row in cursor:
        return row[0]


def split_sentence(text, num_of_words):
    list_words = text.split(" ")
    length = len(list_words)
    splitted_sentence = []
    b_index = 0
    e_index = num_of_words
    while length > 0:
        part = ""
        for word in list_words[b_index:e_index]:
            part = part + " " + word
        splitted_sentence.append(part)
        b_index += num_of_words
        e_index += num_of_words
        length -= num_of_words
    return splitted_sentence


def put_splitted_text_in_blackboard(blackboard, splitted_text):
    y = 200
    for text in splitted_text:
        cv2.putText(blackboard, text, (4, y), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
        y += 50


def get_hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist


def recognize():
    global prediction
    cam = create_cam_obj()
    hist = get_hand_hist()
    x, y, w, h = 300, 100, 300, 300
    while True:
        text = ""
        img, thresh = preprocess(cam, h, hist, w, x, y)
        contours = resolve_contour_based_on_cv_version(thresh)
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 10000:
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                save_img = thresh[y1:y1 + h1, x1:x1 + w1]
                if w1 > h1:
                    save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))
                elif h1 > w1:
                    save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))

                pred_probab, pred_class = keras_predict(model, save_img)

                if pred_probab * 100 > 80:
                    text = get_pred_text_from_db(pred_class)
                    print(text)
        show(h, img, text, thresh, w, x, y)
        if cv2.waitKey(1) == ord('q'):
            break


def resolve_contour_based_on_cv_version(thresh):
    (openCV_ver, _, __) = cv2.__version__.split(".")
    if openCV_ver == '3':
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
    elif openCV_ver == '4':
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    else:
        raise Exception("Unsupported version of open cv")
    return contours


def create_cam_obj():
    cam = cv2.VideoCapture(1)
    if cam.read()[0] == False:
        cam = cv2.VideoCapture(0)
    return cam


def show(h, img, text, thresh, w, x, y):
    blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
    splitted_text = split_sentence(text, 2)
    put_splitted_text_in_blackboard(blackboard, splitted_text)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    res = np.hstack((img, blackboard))
    cv2.imshow("Recognizing gesture", res)
    cv2.imshow("thresh", thresh)


keras_predict(model, np.zeros((50, 50), dtype=np.uint8))
recognize()
