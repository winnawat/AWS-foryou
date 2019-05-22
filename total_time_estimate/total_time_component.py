"""this module is the total time estimation component"""
import copy
import unittest
import warnings
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

warnings.filterwarnings('ignore')


def func_log(x, a):
    """A logarithmic function with y-intercept equal to zero"""
    y = a*np.log(x)
    return y


def func_sqrd(x, a):
    """A squaring function with y-intercept equal to zero"""
    y = a*np.power(x, 2)
    return y


def func_linear(x, a):
    """A linear function with y-intercept equal to zero"""
    y = a*x
    return y


def find_total_time(times, row_percents=[1, 5, 10]):
    """Given a list of three times and the percentages of a data set used to \
    calculate those times, this function will estimate the time required to \
    run the entire data set."""
    popt_linear, pcov_linear = curve_fit(func_linear,  row_percents, times)
    resid_linear = np.linalg.norm(times-func_linear(row_percents, popt_linear))
    popt_sqrd, pcov_sqrd = curve_fit(func_sqrd,  row_percents,  times)
    resid_sqrd = np.linalg.norm(times-func_sqrd(row_percents, popt_sqrd))
    popt_log, pcov_log = curve_fit(func_log,  row_percents,  times)
    resid_log = np.linalg.norm(times-func_log(row_percents, popt_log))
    total_time = -1
    best_fit = np.min([resid_linear, resid_sqrd, resid_log])

    if best_fit == resid_linear:
        x_shape_param = popt_linear[0]
        total_time = func_linear(100, x_shape_param)
    elif best_fit == resid_sqrd:
        x_shape_param = popt_sqrd[0]
        total_time = func_sqrd(100, x_shape_param)
    else:
        x_shape_param = popt_log[0]
        total_time = func_log(100, x_shape_param)

    return total_time
