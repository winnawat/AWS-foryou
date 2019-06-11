"""
Module that runs a simple perceptron on MNIST dataset.
"""

import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils


def baseline_model(num_pixels, num_classes):
    """
    :param num_pixels: number of pixels in input pictures
    :param num_classes: number of classes
    :return: keras model
    """

    # create model
    model = Sequential()
    model.add(Dense(num_pixels, input_dim=num_pixels,
                    kernel_initializer='normal', activation='relu'))
    model.add(Dense(num_classes, kernel_initializer='normal',
                    activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    return model


def run_mnist(data_loc, target_loc):
    """
    :param data_loc: location of training and test data
    :param target_loc: location of target
    :return: None
    """
    np.random.seed(47)

    data = pd.read_csv(data_loc, index_col=0)
    target = pd.read_csv(target_loc, index_col=0)

    data_shape = data.shape[0]
    train_shape = int(np.floor(data_shape * 0.8))

    x_train = data.iloc[:train_shape, :]
    x_test = data.iloc[train_shape:, :]

    y_train = target.iloc[:train_shape]
    y_test = target.iloc[train_shape:]

    # Normalize inputs from 0-255 to 0-1
    x_train = x_train / 255
    x_test = x_test / 255

    # One hot encode outputs
    y_train = np_utils.to_categorical(y_train)
    y_test = np_utils.to_categorical(y_test)
    num_pixels = x_train.shape[1]
    num_classes = y_test.shape[1]

    # Build the model
    model = baseline_model(num_pixels, num_classes)

    # Fit the model
    model.fit(x_train, y_train, epochs=10, batch_size=200, verbose=0,
              validation_data=(x_test, y_test))

    return None
