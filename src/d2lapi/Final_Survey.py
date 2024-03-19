import pandas as pd
import numpy as np


def createSurveyOrder(survey_details):
    '''
    This creates a unique order of questions for every survey. Fixes/ used to fixed the following
    question numbers to determine "end" of questions for binary question format 

    inputs:
    survey details is the data that you are attempting to transform/ modified (with answer key) question details file

    outputs:
    survey detail with ordered question parts for each user
    '''
    survey_details['Q Text'] = survey_details['Q Text'].apply(lambda x: str(x).replace(u'\xa0', u''))
    d = dict(enumerate(survey_details["Q Text"].unique(), 1))
    reversed_d = dict([(value, key) for key, value in d.items()])
    survey_details['label'] = survey_details['Q #'].astype(str) + survey_details.groupby(['User', 'Q #']). \
        cumcount().add(1).astype(str)
    survey_details.insert(9, "Q #", survey_details.pop("Q #"))
    survey_details['Q Text'] = survey_details['Q Text'].apply(lambda x: str(x).replace(u'\xa0', u''))

    return survey_details


def nullRowChecker(row, user_arr):
    '''
    checks whether a row does not have a value

    inputs:
    row: a row value
    user_arr: an empty Python list

    outputs:
    Nan: returns absent value to row in orginal dataframe column if row originally was not null.
    user_arr[-1]: returns value in user_arr if row value is not null
    '''
    if pd.notna(row):
        user_arr.append(row)
        return np.nan
    elif pd.isna(row):
        return user_arr[-1]


# append the "answerkey" to the top of the dataframe. (should be used before quiz order)
def csvWithUserColumn(survey_details):
    '''
    append the "answerkey" to the top of the dataframe. (should be used before quiz order)

    inputs:
    survey_details: the survey_details dataframe

    outputs:
    survey_details: survey_details dataframe with modified 'Section #' column
    '''
    user_lst = []
    survey_details['Section #'] = survey_details['Section #'].apply(lambda x: nullRowChecker(x, user_lst))
    survey_details = survey_details[survey_details['Section #'].notna()]
    survey_details = survey_details.rename(columns={"Section #": "User"})
    return survey_details


def trufalse_mc_check(response):
    '''
    checks whether a True/False, multiple choice, or multi-select question is checked 
    or not based on the response value

    inputs:
    response: a row value with value of 1.0000 or 0

    outputs:
    1: binary value representing a response value of 1.00000
    0: binary value representing a response value of 0
    '''
    return 0 if response == 0.000 else response


def answer_match_check(answer_match):
    '''
    returns the answer for matching, ordering, short-answer, multiple-short answer or
    free-response questions

    inputs:
    answer_match: a row value with student response as string in "Answer Match" column

    outputs:
    answer_match: a row value with student response as string in "Answer Match" column
    '''
    return answer_match


def answer_check(answer):
    '''
    returns the answer for written-response questions

    inputs:
    answer: a row value with student response as string in "Answer" column

    outputs:
    answer: a row value with student response as string in "Answer" column
    '''
    return answer


def question_df_creation(official):
    '''
    Creates dataframe with answers for each whole question(needs to be optimized)

    inputs:
    official: the modified survey details dataframe

    outputs:
    returns dataframe with user, question whole number and answer columns 
    '''
    wide_format_df = pd.DataFrame(columns=['User', 'Question #', 'Answer'])

    # Create a dictionary that maps each question type to the corresponding column in the 'official' dataframe
    qtype_map = {'T/F': 'trufalse_mc_check', 'M-S': 'trufalse_mc_check', 'MC': 'trufalse_mc_check',
                 'MAT': 'answer_match_check', 'ORD': 'answer_match_check', 'SA': 'answer_match_check',
                 'MSA': 'answer_match_check', 'FIB': 'answer_match_check', 'WR': 'answer_check',
                 'LIK': 'answer_match_check'}

    # Map each question to its corresponding column using the 'qtype_map' dictionary
    qtype_col = official['Q Type'].map(qtype_map)

    # Assign values to each column in the 'wide_format_df' dataframe using vectorized operations
    wide_format_df['User'] = official['User']
    wide_format_df['Question #'] = official['label']
    wide_format_df['Answer'] = qtype_col

    # Apply relevant mask function to the relevant rows using a boolean mask
    # to avoid applying it to rows that don't need it
    mask = qtype_col == 'trufalse_mc_check'
    mask2 = qtype_col == 'answer_match_check'
    mask3 = qtype_col == 'answer_check'

    wide_format_df.loc[mask, 'Answer'] = official[official['Q Type'].isin(['T/F', 'MC', 'M-S'])]['# Responses'] \
        .apply(lambda x: trufalse_mc_check(x))

    mask_lik_mat_ord = official['Q Type'].isin(['LIK', 'MAT', 'ORD'])
    mask_sa_msa_fib = official['Q Type'].isin(['SA', 'MSA', 'FIB'])

    if mask_lik_mat_ord.any():
        responses = official[mask_lik_mat_ord]['# Responses']
        wide_format_df.loc[mask2 & mask_lik_mat_ord, 'Answer'] = responses.apply(lambda x: answer_match_check(x))

    if mask_sa_msa_fib.any():
        answer_match = official[mask_sa_msa_fib]['Answer Match']
        wide_format_df.loc[mask2 & mask_sa_msa_fib, 'Answer'] = answer_match.apply(lambda x: answer_match_check(x))

        wide_format_df.loc[mask3, 'Answer'] = official[official['Q Type'] == 'WR']['Answer'] \
            .apply(lambda x: answer_match_check(x))

    # Select the required columns and return the resulting dataframe
    return wide_format_df[['User', 'Question #', 'Answer']]

def qa_label_dataframe(new_data):
    ''' 
    Creates dataframe that serves as a key for question and answer labels in the final output.

    inputs:
    new_data: the modified_details dataframe
    
    outputs:
    the label dataframe consisting of new label, question text, and answer text. 
    '''

    df_list = []
    for index, row in new_data.iterrows():
        if (row['Q Type'] == 'FIB') or (row['Q Type'] == 'WR') or ( row['Q Type'] == 'SA') or ( row['Q Type'] == 'MSA'):
            new_list = [('Q'+ str(row['label'])), row['Q Text'], '']
        else:
            new_list = [('Q'+ str(row['label'])), row['Q Text'], row['Answer']]
        df_list.append(new_list)
    answers_df = pd.DataFrame(df_list, columns =['Q Label', 'Question Text', 'Answer Text'])
    unique_answers_df = answers_df.drop_duplicates()
    unique_answers_df = unique_answers_df.set_index('Q Label')
    return unique_answers_df

def question_df_column_list_creation(new_data):
    '''
    Creates a dataframe with questions

    Returns a list of question columns for the question whole dataframe

    inputs:
    new_data: the question whole dataframe

    outputs:
    list containing questions of dataframe for every user
    '''
    temp_columns = []
    q_list = []

    for question in new_data['Question #']:
        if question not in q_list:
            q_list.append(question)
            temp_columns.append(str(question))
        elif question in q_list:
            q_list = []
            break

    return temp_columns


def question_df_pivot(question_df, col_list):
    '''
    Creates a wide binary format of the question whole dataframe

    inputs:
    question_df: the question whole dataframe
    col_list: list containing questions of dataframe for every user except the "answerkey" user

    outputs:
    mod_question_df: pivotted question whole dataframe with question whole column renaming
    '''
    mod_question_df = pd.pivot_table(question_df, index=['User'],
                                     values='Answer', columns=['Question #'], aggfunc='first')
    mod_question_df = mod_question_df.reindex(col_list, axis=1)
    mod_question_df.columns = ['Q' + str(i) for i in mod_question_df.columns]
    return mod_question_df

def completeSurvey(attemptdetails, qa_label_key = False):
    '''
    converts csv data into a wide, binary format using functions

    inputs:
    attemptdetails: the data that contains survey details
    qa_label_key: A boolean that allows you to set if you want the question and answer label key outputted along with the final data output. It's default is false (no label key), but true will return the label key as well. 
    


    outputs:
    wide_format_data: the wide, binary formatted dataframe where 0 and 1 represent checked or 
    unchecked for question parts and correct or incorrect answers. For questions other than 
    True/False, MC, or M-S, the dataframe outputs the user answer

    if qa_label_key is true:
        qa_label_df: the label dataframe consisting of new label, question text, and answer text. 

    '''
    survey_details = pd.read_csv(attemptdetails)
    survey_details_with_user_column = csvWithUserColumn(survey_details)
    mod_survey_details = createSurveyOrder(survey_details_with_user_column)
    question_df = question_df_creation(mod_survey_details)
    qa_label_data = qa_label_dataframe(mod_survey_details)
    question_df_col_list = question_df_column_list_creation(question_df)
    wide_format_data = question_df_pivot(question_df, question_df_col_list)
    if qa_label_key == True:
        return wide_format_data, qa_label_data
    else:
        return wide_format_data




