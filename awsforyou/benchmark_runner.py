"""
Script that trains a simply perceptron using the keras library on the MNIST
dataset. This script is used as a benchmark test for EC2 clusters.
"""

# import benchmark_runner
# benchmark_runner.run_benchmark()

from datetime import datetime, timezone
import numpy as np
import os
import pandas as pd
import sys
import time

from cpuinfo import get_cpu_info
from keras.datasets import mnist
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils
import psutil

# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def write_scorecard(dict):
    """
    Append the aws-scorecard using the string input.
    """
    results = pd.DataFrame([dict])
    try:
        scorecard = pd.read_csv('./aws-scorecard.csv')
        scorecard = pd.concat([scorecard, results], sort=False)
        # print("csv exists")
    except Exception:
        # print("csv does not exist")
        scorecard = results

    scorecard.set_index('datetime', inplace=True)
    scorecard.to_csv('./aws-scorecard.csv')
    return None


def get_data():
    # the data, shuffled and split between tran and test sets
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype("float32") / 255
    X_test = X_test.astype("float32") / 255

    # convert class vectors to binary class matrices
    y_train = np_utils.to_categorical(y_train)
    y_test = np_utils.to_categorical(y_test)

    return (X_train, y_train), (X_test, y_test)


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
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    return model


def run_full_mnist(X_train, y_train, X_test, y_test):
    """
    :param X_train: location of training and test data
    :param y_test: location of target
    :return: None
    """
    # build the model
    num_pixels = X_train.shape[1]
    num_classes = y_test.shape[1]
    model = baseline_model(num_pixels, num_classes)
    # Fit the model
    model.fit(X_train, y_train, epochs=10, batch_size=200, verbose=2,
              validation_data=(X_test, y_test))


def run_benchmark(aws=False):
    """
    Runs the benchmark (keras_mnist_3) on full data.
    Append/generate results file called 'AWS-scorecard'
    scorecard contains system information and runtime
    """
    results = {}

    if aws is True:
        import get_aws_instance
        instancetype_region = get_aws_instance.get_instance()
        results['instancetype'] = instancetype_region['instancetype']
        results['region'] = instancetype_region['region']
    else:
        results['instancetype'] = 'local-machine'
        results['region'] = 'local-machine'
        pass

    results['datetime'] = datetime \
        .now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    results['timezone'] = 'UTC'

    for key, value in get_cpu_info().items():
        results[key] = value
    mem = psutil.virtual_memory()
    results['RAM'] = int(round(mem.total/(1024*1024*1000), 0))

    # locate data here (temporary)
    (X_train, y_train), (X_test, y_test) = get_data()
    # data = '../mnist_data/data_10.csv'
    # target = '../mnist_data/target_10.csv'
    # finish locating data

    # run and time mnist
    start = time.time()
    run_full_mnist(X_train, y_train, X_test, y_test)
    # keras_mnist_3.run_mnist(data, target)
    finish = time.time()
    runtime = finish - start
    results['runtime'] = runtime
    write_scorecard(results)

    print("mnist runtime: %f " % runtime)
    return runtime
