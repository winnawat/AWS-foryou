
import os
import pandas as pd
from awsforyou import total_time_component
from awsforyou import algo_runner
import matplotlib.pyplot as plt
from keras.datasets import mnist


def demo(num_pts=3, num_iter=3):
    """
    A demonstration of the time-prediction components of our program.
    :param python_call: str python string calling the algorithm to be timed
    :param module_name: name of module from which function is called
    :param num_pts: number of points to consider
    :param num_iter: number of iterations over points
    :return: tot_time the predicted time to run on 100% of data in seconds.
    """
    # Download MNIST data:
    print('Loading mnist dataset...')
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    print('Finished loading mnist dataset.')

    # flatten 28*28 images to a 784 vector for each image
    num_pixels = X_train.shape[1] * X_train.shape[2]
    X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
    X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

    data = pd.concat([pd.DataFrame(X_train), pd.DataFrame(X_test)], axis=0)

    # y_train = np_utils.to_categorical(y_train)
    # y_test = np_utils.to_categorical(y_test)

    target = pd.concat([pd.DataFrame(y_train), pd.DataFrame(y_test)], axis=0)

    this_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(this_dir + '/data'):
        os.mkdir(this_dir + '/data')

    # Data and target to csv
    print('Saving data to disk.')
    data.to_csv('data/mnist_data.csv')
    target.to_csv('data/mnist_target.csv')
    print('Finished saving data to disk.')

    # Create python call
    PYTHON_CALL = "run_mnist(data_loc = 'data/mnist_data.csv', target_loc = " \
                  "'data/mnist_target.csv')"
    MODULE_NAME = 'awsforyou.tests.test_keras_mnist'

    print('Running algo_runner, this may take a few moments.')
    times, percents = algo_runner.run_algo(PYTHON_CALL, MODULE_NAME,
                                           num_pts, num_iter)
    tot_time = total_time_component.find_total_time(times, percents)[0]
    print('Finished algo_runner.')

    print('Removing data files.')
    os.remove('data/mnist_data.csv')
    os.remove('data/mnist_target.csv')

    all_times = [times[0]]
    all_percents = [percents[0]]
    all_times.append(tot_time)
    all_percents.append(100)

    print('Plotting results.')
    plt.plot(percents, times, 'ro')
    plt.plot(all_percents, all_times, 'b', linewidth=2)
    plt.xlim(0, max(tot_time + 0.1*tot_time, 100))
    plt.ylim(0, max(tot_time + 0.1*tot_time, 100))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    return tot_time
