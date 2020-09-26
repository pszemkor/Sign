import cv2, pickle
import numpy as np
import json
from keras.preprocessing import image

prediction = None


def get_image_size():
    return (200, 200)


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


def keras_predict(model, img):
    img = image.smart_resize(img, size=(200, 200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images)
    max_id, max_prob = -1, -1
    for i in range(len(classes[0])):
        if classes[0][i] > max_prob:
            max_id = i
            max_prob = classes[0][i]
    return max_prob, max_id


def get_pred_label(pred_class):
    with open("gestures.json") as gestures:
        class_label = json.load(gestures)
        return class_label[str(pred_class)]

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


def show(h, img, w, x, y):
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
    cv2.imshow("Recognizing gesture", img)
