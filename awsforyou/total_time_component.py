"""this module is the total time estimation component"""
import warnings
import numpy as np
from scipy.optimize import curve_fit

warnings.filterwarnings('ignore')


def func_log(data, a_factor, y_int):
    """A logarithmic function with y-intercept"""
    return a_factor * np.log(data) + y_int


def func_nlogn(data, a_factor, y_int):
    """A n*log(n) function with y-intercept"""
    return a_factor * data * np.log(data) + y_int


def func_linear(data, a_factor, y_int):
    """A linear function with y-intercept"""
    return a_factor * data + y_int

def func_sqrd(data, a_factor, y_int):
    """A squaring function with y-intercept"""
    return a_factor * data**2 + y_int


def find_total_time(times, row_percents=(1, 5, 10)):
    """Given a list of three times and the percentages of a data set used to \
    calculate those times, this function will estimate the time required to \
    run the entire data set."""
    popt_linear = curve_fit(func_linear, row_percents, times)[0]
    a_linear = popt_linear[0].flatten()
    b_linear = popt_linear[1].flatten()
    resid_linear = np.linalg.norm(times-func_linear(row_percents,
                                                    a_linear, b_linear))

    popt_log = curve_fit(func_log, row_percents, times)[0]
    a_log = popt_log[0].flatten()
    b_log = popt_log[1].flatten()
    resid_log = np.linalg.norm(times-func_log(row_percents, a_log, b_log))

    popt_nlogn = curve_fit(func_nlogn, row_percents, times)[0]
    a_nlogn = popt_nlogn[0].flatten()
    b_nlogn = popt_nlogn[1].flatten()
    resid_nlogn = np.linalg.norm(times - func_nlogn(row_percents,
                                                    a_nlogn, b_nlogn))

    popt_sqrd = curve_fit(func_sqrd, row_percents, times)[0]
    a_sqrd = popt_sqrd[0].flatten()
    b_sqrd = popt_sqrd[1].flatten()
    resid_sqrd = np.linalg.norm(times - func_sqrd(row_percents,
                                                    a_sqrd, b_sqrd))

    best_fit = np.min([resid_linear, resid_nlogn, resid_log, resid_sqrd])

    if best_fit == resid_linear:
        total_time = func_linear(100, a_linear, b_linear)
        model = ["linear", a_linear, b_linear]
    elif best_fit == resid_nlogn:
        total_time = func_nlogn(100, a_nlogn, b_nlogn)
        model = ["nlogn", a_nlogn, b_nlogn]
    elif best_fit == resid_sqrd:
        total_time = func_sqrd(100, a_sqrd, b_sqrd)
        model = ["sqrd", a_sqrd, b_sqrd]
    else:
        total_time = func_log(100, a_log, b_log)
        model = ["log", a_log, b_log]

    output = [total_time/3600] + [model]

    return output

