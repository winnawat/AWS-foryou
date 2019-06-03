"""this module is the total time estimation component"""
import warnings
import numpy as np
from scipy.optimize import curve_fit

warnings.filterwarnings('ignore')


def func_log(x, a, b):
    """A logarithmic function with y-intercept equal to zero"""
    y = a * np.log(x) + b
    return y


def func_sqrd(x, a, b):
    """A squaring function with y-intercept equal to zero"""
    y = a*np.power(x, 2)+b
    return y


def func_linear(x, a, b):
    """A linear function with y-intercept equal to zero"""
    y = a * x + b
    return y


def find_total_time(times, row_percents=(1, 5, 10)):
    """Given a list of three times and the percentages of a data set used to \
    calculate those times, this function will estimate the time required to \
    run the entire data set."""
    popt_linear, pcov_linear = curve_fit(func_linear,  row_percents, times)
    a_linear = popt_linear[0].flatten()
    b_linear = popt_linear[1].flatten()
    resid_linear = np.linalg.norm(times-func_linear(row_percents,
                                                    a_linear, b_linear))

    popt_sqrd, pcov_sqrd = curve_fit(func_sqrd,  row_percents,  times)
    a_sqrd = popt_sqrd[0].flatten()
    b_sqrd = popt_sqrd[1].flatten()
    resid_sqrd = np.linalg.norm(times-func_sqrd(row_percents, a_sqrd, b_sqrd))

    popt_log, pcov_log = curve_fit(func_log,  row_percents,  times)
    a_log = popt_log[0].flatten()
    b_log = popt_log[1].flatten()
    resid_log = np.linalg.norm(times-func_log(row_percents, a_log, b_log))

    best_fit = np.min([resid_linear, resid_sqrd, resid_log])

    if best_fit == resid_linear:
        total_time = func_linear(100, a_linear, b_linear)
    elif best_fit == resid_sqrd:
        total_time = func_sqrd(100, a_sqrd, b_sqrd)
    else:
        total_time = func_log(100, a_log, b_log)

    return total_time
