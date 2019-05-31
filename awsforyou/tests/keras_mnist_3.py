"""
Module that runs a simple perceptron on MNIST dataset.
"""

import os
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# define baseline model
def baseline_model(num_pixels, num_classes):
    """
    :param num_pixels: number of pixels in input pictures
    :param num_classes: number of classes
    :return: keras model
    """

    # create model
    model = Sequential()
    model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal',
                    activation='relu'))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def run_mnist(data_loc, target_loc):
    """
    :param data_loc: location of training and test data
    :param target_loc: location of target
    :return: None
    """
    seed = 7
    np.random.seed(seed)
    print('loading data.csv')
    X = pd.read_csv(data_loc, index_col=0)

    print('loading target.csv')
    y = pd.read_csv(target_loc, index_col=0)

    data_shape = X.shape[0]
    train_shape = int(np.floor(data_shape * 0.8))

    X_train = X.iloc[:train_shape, :]
    X_test = X.iloc[train_shape:, :]

    y_train = y.iloc[:train_shape]
    y_test = y.iloc[train_shape:]

    X = np.array(X)
    y = np.array(y)

    # Normalize inputs from 0-255 to 0-1
    X_train = X_train / 255
    X_test = X_test / 255

    # one hot encode outputs
    y_train = np_utils.to_categorical(y_train)
    y_test = np_utils.to_categorical(y_test)
    num_pixels = X_train.shape[1]
    num_classes = y_test.shape[1]

    # build the model
    model = baseline_model(num_pixels, num_classes)

    # Fit the model
    model.fit(X_train, y_train, epochs=10, batch_size=200, verbose=2,
              validation_data=(X_test, y_test))

    return None
