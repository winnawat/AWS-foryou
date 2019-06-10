"""
Script that trains a simply perceptron using the keras library on the MNIST
dataset. This script is used as a benchmark test for EC2 clusters.
"""

from datetime import datetime, timezone
import time

import pandas as pd
from cpuinfo import get_cpu_info
from keras.datasets import mnist
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils
import psutil

from awsforyou import aws_metadata


def write_scorecard(results_dict):
    """
    Append the aws-scorecard using the dictionary input.
    """

    results = pd.DataFrame([results_dict])
    try:
        scorecard = pd.read_csv('./aws-scorecard.csv')
        scorecard = pd.concat([scorecard, results], sort=False)
    except FileNotFoundError:
        scorecard = results
    except Exception:
        print("reading CSV encountered an error")
        raise

    scorecard.set_index('datetime', inplace=True)
    scorecard.to_csv('./aws-scorecard.csv')


def get_data():
    """
    Script to download data from keras.datasets mnist.
    60k rows of training set.
    10k rows of test set.
    No input.
    returns (x_train, y_train), (x_test, y_test)
    """
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # convert class vectors to binary class matrices
    y_train = np_utils.to_categorical(y_train)
    y_test = np_utils.to_categorical(y_test)

    return x_train, y_train, x_test, y_test


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


def run_full_mnist(x_train, y_train, x_test, y_test):
    """
    :param x_train: numpy array - training set features
    :param y_train: numpy array - training set targets
    :param x_test: numpy array - test set features
    :param y_test: numpy array - test set targets
    :return: None
    """
    # build the model
    num_pixels = x_train.shape[1]
    num_classes = y_test.shape[1]
    model = baseline_model(num_pixels, num_classes)
    # Fit the model
    model.fit(x_train, y_train, epochs=10, batch_size=200, verbose=0,
              validation_data=(x_test, y_test))


def run_benchmark(aws=False):
    """
    Runs the benchmark on full mnist data.
    Append/generate results file called 'aws-scorecard'
    scorecard contains system information and runtime
    :param aws=False: If set to True, the script will fetch
    AWS instance information. This will throw an error if run on local machine.
    returns runtime
    """
    results = {}

    if aws is True:
        instancetype_region = aws_metadata.get_instance()
        results['instancetype'] = instancetype_region['instancetype']
        results['region'] = instancetype_region['region']
    else:
        results['instancetype'] = 'local-machine'
        results['region'] = 'local-machine'

    results['datetime'] = datetime \
        .now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    results['timezone'] = 'UTC'

    for key, value in get_cpu_info().items():
        results[key] = value
    mem = psutil.virtual_memory()
    results['RAM'] = int(round(mem.total/(1024*1024*1000), 0))

    # getting data
    x_train, y_train, x_test, y_test = get_data()

    # run and time mnist
    start = time.time()
    run_full_mnist(x_train, y_train, x_test, y_test)
    finish = time.time()
    runtime = finish - start
    results['runtime'] = runtime

    if aws is True:
        write_scorecard(results)

    print("mnist runtime: %f " % runtime)
    return runtime
