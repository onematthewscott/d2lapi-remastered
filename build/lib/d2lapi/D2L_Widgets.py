# importing pandas library
import pandas as pd

# importing numpy library
import numpy as np

# importing ipywidget library
import ipywidgets as widgets

# importing matplotlib library
import matplotlib.pyplot as plt

#importing io library
import io

# importing display help
from IPython.display import Javascript, display

def File_Upload_Convert(input_file_widget_value):
    '''
    Function that prepares file input from file upload widget to be input into
    quiz / survey cleaning function
    
    inputs:
    input_file_widget_value: result from file upload widget - .csv that was uploaded
    
    outputs:
    final_content: byte object that can be passed into pd.read_csv
    '''
    try:
        input_file = list(input_file_widget_value.values())[0]
        input_file_content = input_file['content']
        final_content = io.BytesIO(input_file_content)
        return final_content
    except IndexError:
        return ''

def run_1(self):
    '''
    Helper function for use with buttons to run one cell below

    '''
    # #reference for running cells programmatically
    # https://stackoverflow.com/questions/64437714/jupyter-notebook-run-cell-programmatically
    display(Javascript('IPython.notebook.execute_cells_below(1)'))

def run_2(self):
    '''
    Helper function for use with buttons to run two cells below

    '''
    # #reference for running cells programmatically
    # https://stackoverflow.com/questions/64437714/jupyter-notebook-run-cell-programmatically
    display(Javascript('IPython.notebook.execute_cells_below(2)'))

def f(x):
    '''
    Simple helper function for working with widgets
    '''
    return x