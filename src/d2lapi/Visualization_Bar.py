# Function definitions for visualization

# importing pandas library
import pandas as pd

# importing numpy library
import numpy as np

# importing ipywidget library
import ipywidgets as widgets

# importing matplotlib library
import matplotlib.pyplot as plt

# helper function to determine number of questions in a quiz / maximum question number since quizzes are variable
def get_max_q_number(df):

    '''
    Helper function to determine number of questions in a quiz / maximum question number since quizzes are variable
    
    inputs:
    df: Your converted data that you want to use for your bar graph
    
    outputs:
    user_attempt: dataframe that contains ordered questions as well as ordered question parts
    '''

    # get list of columns in dataset
    col_list = list(df.columns)

    # get only columns that refer to questions (i.e. no username, etc)
    question_col_list = []
    for element in col_list:
        # we can determine which are question columns based on whether they have a Q and a number
        if (element[0] == 'Q') & (element[1].isdigit() == True):
            question_col_list.append(element)
    
    # starting point for iteration
    max_q_num = 0
    # loop through question columns
    for element in question_col_list:
        # get number out of column names
        # reference for use of split
        # https://stackoverflow.com/questions/27387415/how-would-i-get-everything-before-a-in-a-string-python
        question_num = int(element[1:].split('.')[0])
        # if the number that was parsed is larger than our current max, save it
        if question_num > max_q_num:
            max_q_num = question_num
    # return final max question number
    return max_q_num

def create_bar(df, dropdown_value):
    
    # get max question number with helper function
    max_q_num = get_max_q_number(df)
    
    # refer to value selected in widget
    # column_num = dropdown_value.value
    column_num = dropdown_value
    
    # if we are looking at a specific question and not total
    if column_num != 'Total':
        # make the column name we want to access using question number
        column_name = 'Q'+ dropdown_value.value +'.0'
        # check that it is compatible with current scoring algorithm
        if type(max(df[column_name].unique())) is not str:
            # save data frame with unique values and their frequencies
            saved_values = df[column_name].value_counts()
            
            # take out the answer key's score
            # We still want to be able to access information from the answer key,
            # we just don't want it to increment the final total
            saved_values[max(saved_values.index)] = saved_values[max(saved_values.index)] - 1
            
            # create the figure with set size
            fig1, ax1 = plt.subplots(figsize = (12,5))
            
            # figure settings
            # bar plot in MSU green
            # reference for bar plot with value counts: 
            # https://www.kaggle.com/code/tejainece/seaborn-barplot-and-pandas-value-counts
            # MSU brand colors: https://brand.msu.edu/visual/color-palette
            ax1.bar(saved_values.index, saved_values.values, color = '#18453B')
            # set appropriate tick values and limits (answer key score is useful for this)
            ax1.set_xticks(list(range(0, max(df[column_name].unique())+1)))
            ax1.set_yticks(list(range(0, max(df[column_name].value_counts()) + 3)))
            # adjust size for tick labels
            # reference for tick params:
            # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
            ax1.tick_params(axis='both', which='major', labelsize=12)
            # put frequency labels on bars to make it quicker to understand
            # reference for bar label:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar_label.html
            ax1.bar_label(ax1.containers[0], size = 14)
            # give the graph a title
            ax1.set_title("Score Distribution for Question " + dropdown_value.value, size = 22)
            # give the graph axis labels
            ax1.set_xlabel("Score on Question " + dropdown_value.value, size = 18)
            ax1.set_ylabel("Count", size = 18)
            
            # return the figure we made
            return fig1
        else:
            # if it isn't compatible with current scoring, we can't make the graph and we let the user know
            print('WARNING: This question type is not compatible with this visualization')
    if column_num == 'Total':
        
        # get total scores by looping through students and summing score on each question
        
        # start with empty list
        score_list = []
        # loop through students
        for row in range(0, df.shape[0]):
            total_score = 0
            # loop through questions
            for i in range(1, max_q_num + 1):
                # get column name for question we want to access
                column_name = 'Q'+ str(i) +'.0'
                # if it is compatible with current scoring
                if type(max(df[column_name].unique())) is not str:
                    # if it is not na
                    if np.isnan(df[column_name][row]) == False:
                        # increment total score
                        total_score += df[column_name][row]
            # add calculated score to total
            score_list.append(total_score)
        
        score_df = pd.DataFrame({'scores': score_list})
        saved_scores = score_df['scores'].value_counts()
        
        # take out the answer key's score
        # We still want to be able to access information from the answer key,
        # we just don't want it to increment the final total
        saved_scores[max(saved_scores.index)] = saved_scores[max(saved_scores.index)] - 1
        
        # create the figure with set size
        fig, ax = plt.subplots(figsize = (12,5))
        
        # figure settings
        # bar plot in MSU green
        ax.bar(saved_scores.index, saved_scores.values, color = '#18453B')
        # set appropriate tick values and limits (answer key score is useful for this)
        ax.set_xticks(list(range(0, max(score_df['scores'].unique())+1)))
        ax.set_yticks(list(range(0, max(score_df['scores'].value_counts()) + 3)))
        # adjust size for tick labels
        ax.tick_params(axis='both', which='major', labelsize=12)
        # put frequency labels on bars to make it quicker to understand
        ax.bar_label(ax.containers[0], size = 14)
        # give the graph a title
        ax.set_title("Total Score Distribution", size = 22)
        # give the graph axis labels
        ax.set_xlabel("Score on Question " + dropdown_value, size = 18)
        ax.set_ylabel("Count", size = 18)
        
        # return the figure we made
        return fig

def create_interactive_bar(df, dropdown_value):
    # reference, matplotlib documentation for barplot: 
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html

    # get max question number with helper function
    max_q_num = get_max_q_number(df)
    
    
    # if we are looking at a specific question and not total
    if dropdown_value != 'Total':
        # make the column name we want to access using question number
        column_name = 'Q'+ dropdown_value +'.0'
        # check that it is compatible with current scoring algorithm
        if type(max(df[column_name].unique())) is not str:
            # save data frame with unique values and their frequencies
            saved_values = df[column_name].value_counts()
            
            # take out the answer key's score
            # We still want to be able to access information from the answer key,
            # we just don't want it to increment the final total
            saved_values[max(saved_values.index)] = saved_values[max(saved_values.index)] - 1
            
            # create the figure with set size
            fig1, ax1 = plt.subplots(figsize = (12,5))
            
            # figure settings
            # bar plot in MSU green
            # reference for bar plot with value counts: 
            # https://www.kaggle.com/code/tejainece/seaborn-barplot-and-pandas-value-counts
            # MSU brand colors: https://brand.msu.edu/visual/color-palette
            ax1.bar(saved_values.index, saved_values.values, color = '#18453B')
            # set appropriate tick values and limits (answer key score is useful for this)
            ax1.set_xticks(list(range(0, max(df[column_name].unique())+1)))
            ax1.set_yticks(list(range(0, max(df[column_name].value_counts()) + 3)))
            # adjust size for tick labels
            # reference for tick params:
            # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
            ax1.tick_params(axis='both', which='major', labelsize=12)
            # put frequency labels on bars to make it quicker to understand
            # reference for bar label:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar_label.html
            ax1.bar_label(ax1.containers[0], size = 14)
            # give the graph a title
            ax1.set_title("Score Distribution for Question " + dropdown_value, size = 22)
            # give the graph axis labels
            ax1.set_xlabel("Score on Question " + dropdown_value, size = 18)
            ax1.set_ylabel("Count", size = 18)
            #plt.close()

            # return the figure we made
            return fig1
        else:
            # if it isn't compatible with current scoring, we can't make the graph and we let the user know
            print('WARNING: This question type is not compatible with this visualization')
    if dropdown_value == 'Total':
        
        # get total scores by looping through students and summing score on each question
        
        # start with empty list
        score_list = []
        # loop through students
        for row in range(0, df.shape[0]):
            total_score = 0
            # loop through questions
            for i in range(1, max_q_num + 1):
                # get column name for question we want to access
                column_name = 'Q'+ str(i) +'.0'
                # if it is compatible with current scoring
                if type(max(df[column_name].unique())) is not str:
                    # if it is not na
                    if np.isnan(df[column_name][row]) == False:
                        # increment total score
                        total_score += df[column_name][row]
            # add calculated score to total
            score_list.append(total_score)
        
        score_df = pd.DataFrame({'scores': score_list})
        saved_scores = score_df['scores'].value_counts()
        
        # take out the answer key's score
        # We still want to be able to access information from the answer key,
        # we just don't want it to increment the final total
        saved_scores[max(saved_scores.index)] = saved_scores[max(saved_scores.index)] - 1
        
        # create the figure with set size
        fig, ax = plt.subplots(figsize = (12,5))
        
        # figure settings
        # bar plot in MSU green
        x = ax.bar(saved_scores.index, saved_scores.values, color = '#18453B')
        # set appropriate tick values and limits (answer key score is useful for this)
        ax.set_xticks(list(range(0, max(score_df['scores'].unique())+1)))
        ax.set_yticks(list(range(0, max(score_df['scores'].value_counts()) + 3)))
        # adjust size for tick labels
        ax.tick_params(axis='both', which='major', labelsize=12)
        # put frequency labels on bars to make it quicker to understand
        ax.bar_label(ax.containers[0], size = 14)
        # give the graph a title
        ax.set_title("Total Score Distribution", size = 22)
        # give the graph axis labels
        ax.set_xlabel("Score on Question " + dropdown_value, size = 18)
        ax.set_ylabel("Count", size = 18)
        #plt.close()
        # return the figure we made
        return fig

def f(x):
    return x