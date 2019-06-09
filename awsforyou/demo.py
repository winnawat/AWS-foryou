
import numpy as np
import total_time_component
import algo_runner
import matplotlib.pyplot as plt


def demo(python_call, module_name, num_pts=3, num_iter=3):
    """
    A demonstration of the time-prediction components of our program.
    :param python_call: str python string calling the algorithm to be timed
    :param module_name: name of module from which function is called
    :param num_pts: number of points to consider
    :param num_iter: number of iterations over points
    :return: tot_time the predicted time to run on 100% of data in seconds.
    """
    times, percents = algo_runner.algo_runner(python_call, module_name,
                                              num_pts, num_iter)
    tot_time = total_time_component.find_total_time(times, percents)[0]

    print(tot_time)

    all_times = [times[0]]
    all_percents = [percents[0]]
    all_times.append(tot_time)
    all_percents.append(100)

    print(all_times, all_percents)

    plt.plot(percents, times, 'ro')
    plt.plot(all_percents, all_times, 'b', linewidth=2)
    plt.show()
    return tot_time
