# def classify(img):
#     pass

import keras
import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D, Dense,Flatten, Dropout
from keras.datasets import mnist
from keras.utils.vis_utils import plot_model
from keras.utils import np_utils
from keras.optimizers import SGD
import matplotlib.pyplot as plt
import os
from IPython.display import Image

train = pd.read_csv('sign-language-mnist/sign_mnist_train.csv')
test = pd.read_csv('sign-language-mnist/sign_mnist_test.csv')

y_train = train['label'].values
y_test = test['label'].values

X_train = train.drop(['label'],axis=1)
X_test = test.drop(['label'], axis=1)

X_train = np.array(X_train.iloc[:,:])
X_train = np.array([np.reshape(i, (28,28)) for i in X_train])

X_test = np.array(X_test.iloc[:,:])
X_test = np.array([np.reshape(i, (28,28)) for i in X_test])

num_classes = 26
y_train = np.array(y_train).reshape(-1)
y_test = np.array(y_test).reshape(-1)

y_train = np.eye(num_classes)[y_train]
y_test = np.eye(num_classes)[y_test]

shape_train = (27455, 28, 28, 1)
X_train = X_train.reshape(shape_train)
shape_test = (7172, 28, 28, 1)
X_test = X_test.reshape(shape_test)
classifier = Sequential()
classifier.add(Conv2D(filters=8, kernel_size=(3,3),strides=(1,1),padding='same',input_shape=(28,28,1),activation='relu', data_format='channels_last'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
classifier.add(Conv2D(filters=16, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
classifier.add(Dropout(0.5))
classifier.add(MaxPooling2D(pool_size=(4,4)))
classifier.add(Dense(128, activation='relu'))
classifier.add(Flatten())
classifier.add(Dense(26, activation='softmax'))
classifier.compile(optimizer='SGD', loss='categorical_crossentropy', metrics=['accuracy'])
classifier.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
classifier.fit(X_train, y_train, epochs=50, batch_size=100)
accuracy = classifier.evaluate(x=X_test,y=y_test,batch_size=32)

print("Accuracy: ",accuracy[1])

classifier.summary()
plot_model(classifier, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
plot_model(classifier, show_shapes=True, show_layer_names=True, to_file='model.png')
Image(retina=True, filename='model.png')
classifier.save('SignCNNModel.h5')
