import os
import webbrowser
import pandas as pd
from keras.datasets import mnist
from awsforyou import recommender, report_generator

"""
Main file for running aws_foryou.  Call with python_string and module_name 
and this module will return a sortable data frame that is visualized in a 
browser window.
"""

def aws_foryou(python_call, module_name):

    df = recommender.create_dataframe(python_call, module_name)
    report_generator.generate_report(df)
