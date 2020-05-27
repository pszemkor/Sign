import operator
import string

import cv2
from keras.engine.saving import load_model

from recognize_gesture import create_cam_obj, get_hand_hist, resolve_contour_based_on_cv_version, keras_predict, \
    get_pred_text_from_db, show
from preprocessing import preprocess


model = load_model('cnn_model_keras2.h5')


class RecognitionService():
    def __init__(self):
        super().__init__()
        self.recognized_letters = ['' for i in range(0, 20)]

    def run(self):
        cam = create_cam_obj()
        hist = get_hand_hist()
        x, y, w, h = 300, 100, 300, 300
        while True:
            text = ""
            img, thresh = preprocess(cam, h, hist, w, x, y)
            contours = resolve_contour_based_on_cv_version(thresh)
            if len(contours) > 0:
                contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(contour) > 2000:
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    save_img = thresh[y1:y1 + h1, x1:x1 + w1]
                    if w1 > h1:
                        save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                      cv2.BORDER_CONSTANT, (0, 0, 0))
                    elif h1 > w1:
                        save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                      cv2.BORDER_CONSTANT, (0, 0, 0))

                    pred_probab, pred_class = keras_predict(model, save_img)

                    if pred_probab * 100 > 60:
                        text = get_pred_text_from_db(pred_class)
                        if text in string.ascii_letters.upper():
                            self.recognized_letters.append(text)
                            self.recognized_letters.pop(0)
                            print(text)
            show(h, img, text, thresh, w, x, y)
            if cv2.waitKey(1) == ord('q'):
                break

    def last_letter(self):
        letters_count = {}
        for letter in string.ascii_letters.upper():
            letters_count[letter] = 0
        for letter in self.recognized_letters:
            letters_count[letter] += 1
        return max(letters_count.items(), key=operator.itemgetter(1))[0]
