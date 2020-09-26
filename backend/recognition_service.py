import operator
import string

import cv2
from tensorflow.keras.models import load_model

from backend.preprocessing import preprocess
from backend.recognize_gesture import create_cam_obj, get_hand_hist, resolve_contour_based_on_cv_version, keras_predict, \
    get_pred_label, show

model = load_model('model.h5')


class RecognitionService:
    def __init__(self):
        super().__init__()
        self.recognized_letters = ['$' for i in range(0, 1)]

    def run(self):
        cam = create_cam_obj()
        hist = get_hand_hist()
        x, y, w, h = 300, 100, 300, 300
        while True:
            text = ""
            img, thresh = preprocess(cam, h, hist, w, x, y)
            show(h, img, w, x, y)
            contours = resolve_contour_based_on_cv_version(thresh)
            if len(contours) > 0:
                contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(contour) > 500:
                    img = img[y:y + h, x:x + w, :]
                    pred_probab, pred_class = keras_predict(model, img)
                    if pred_probab * 100 > 60:
                        text = get_pred_label(pred_class)
                        if text in string.ascii_letters.upper():
                            self.recognized_letters.append(text)
                            self.recognized_letters.pop(0)
                            print(text)
            if cv2.waitKey(1) == ord('q'):
                break

    def last_letter(self):
        letters_count = {}
        for letter in string.ascii_letters.upper():
            letters_count[letter] = 0
        for letter in self.recognized_letters:
            if letter not in string.ascii_letters.upper():
                continue
            letters_count[letter] += 1
        return max(letters_count.items(), key=operator.itemgetter(1))[0]
