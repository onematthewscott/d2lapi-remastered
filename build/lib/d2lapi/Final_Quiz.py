from ast import Index

import pandas as pd
import numpy as np

def createQuizOrder(user_attempt, quiz_answer):
    '''
    This creates a unique order of questions for every quiz. Fixes/ used to fixed the following
    question numbers when random ordering on quiz is selected pooling errors used to determine "end" of 
    questions for binary question format 
    
    inputs:
    user_attempt: the data that you are attempting to transform/ modified (with answer key) question details file
    quiz answer: the answer key/question details file
    
    outputs:
    user_attempt: dataframe that contains ordered questions as well as ordered question parts
    '''
    user_attempt['Q Text'] = user_attempt['Q Text'].apply(lambda x: str(x).replace(u'\xa0', u''))
    quiz_answer['Q Text'] = quiz_answer['Q Text'].apply(lambda x: str(x).replace(u'\xa0', u''))
    d = dict(enumerate(quiz_answer["Q Text"].unique(),1))
    reversed_d = dict([(value, key) for key, value in d.items()])
    user_attempt["newQ#"] = user_attempt["Q Text"].apply(lambda x: reversed_d.get(x))
    user_attempt['label']=user_attempt['newQ#'].astype(str)+user_attempt.groupby(['Username','Attempt #','newQ#']).\
        cumcount().add(1).astype(str)
    user_attempt['Q Text'] = user_attempt['Q Text'].apply(lambda x: str(x).replace(u'\xa0', u''))

    return user_attempt

def readincsv (attempt_details, quiz_details):
    '''
    Reads csv file
    
    inputs:
    attempt_details: the data that contains user attempts on questions
    quiz_details: the data that contains quiz answers
    
    outputs:
    user_details: user attempt data as a dataframe
    quiz_details: quiz answers data as a dataframe
    '''
    user_details = pd.read_csv(attempt_details,sep=',')
    user_details = user_details.sort_values(by=['Q Text'])

    quiz_answer_details = pd.read_csv(quiz_details,sep=',')
    quiz_answer_details = quiz_answer_details.sort_values(by=['Q Text'])
    return user_details, quiz_answer_details

def answerKeyOnTop(attempt_details, quiz_details):
    '''
    append the "answerkey" to the top of the dataframe. (should be used before quiz order)
    
    inputs:
    attempt_details: the attempt data dataframe
    quiz_details: the quiz answers data dataframe
    
    outputs:
    attempt_details: modified attempt_details dataframe with "answerkey" user above other users
    '''
    answerkey = quiz_details.copy()
    #answerkey['Org Defined ID'], answerkey["Attempt #"], answerkey ["Username"], answerkey ["FirstName"], \
    #answerkey["LastName"]= ['sdaf@#$345afs#$%&^%^$&%^%^$&asfd*3df',1, "answerKey",
    #                        "Answer", "Key"]
    answerkey['Org Defined ID'], answerkey["Attempt #"], answerkey["Username"], answerkey["FirstName"], \
    answerkey["LastName"] = ['00000000000000000000d#4fgV6Hj!#2fgd]', 1, "answerKey", "Answer", "Key"]
    attempt_details = pd.concat([answerkey,attempt_details ], ignore_index=True )
    return attempt_details

def trufalse_mc_check(answer_match):
    '''
    checks whether a True/False, multiple choice, or multi-select question is checked or not
    based on the answer match tye
    
    inputs:
    answer_match: a row value with "Checked" or "Unchecked" in the "Answer Match" column from the 
    modified attempt_details dataframe
    
    outputs:
    1: binary value representing "Checked"
    0: binary value representing "Unchecked"
    '''
    return 1 if answer_match == 'Checked' else 0

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

def trufalse_mc_score(user_df, idx):
    '''
    Scores True/False, multiple choice, or multi-select questions according to score value
    from the modified_details_dataframe
    
    inputs:
    user_df: the modified_details_dataframe
    idx: the index of the modified_details_dataframe
    
    outputs:
    1: binary value showing that a student scored a question correctly 
    0: binary value showing that a student scored a question incorrectly
    '''
    return 0 if user_df['Score'][idx] < user_df['Out Of'][idx] else 1

def question_dictionary(user_attempt):
    '''
    Creates a dictionary of question:question text key value pairs(For quick question lookup)
    
    inputs: 
    user_attempt: the modified_details dataframe
    
    outputs:
    the question dictionary consisting of question:question text key value pairs
    '''
    return {data["newQ#"]: (data["Q Text"]) for (index, data) in
            user_attempt[user_attempt['Username'] == 'answerKey'].iterrows()}

def qa_label_dictionary(user_attempt):
    ''' 
    Creates dataframe that serves as a key for question and answer labels in the final output.

    inputs:
    user_attempt: the modified_details dataframe
    
    outputs:
    the label dataframe consisting of new label, question text, and answer text. 
    '''
    df_list = []
    for index, row in user_attempt[user_attempt['Username'] == 'answerKey'].iterrows():
        new_list = [('Q'+ str(row['label'])), row['Q Text'], row['Answer']]
        df_list.append(new_list)
    Answers_df = pd.DataFrame(df_list, columns =['Q Label', 'Question Text', 'Answer Text'])
    return Answers_df

def qparts_df_creation(official):
    '''
    Creates a dataframe with question parts
    
    inputs:
    official: the modified_details dataframe
    
    outputs:
    returns dataframe with question part number and answer columns 
    '''
    wide_format_df = pd.DataFrame(columns=['Org Defined ID', 'Attempt #', 'FirstName', 'LastName',
                                           'Question#', 'Answer'])

    # Create a dictionary that maps each question type to the corresponding column in the 'official' dataframe
    qtype_map = {'T/F': 'trufalse_mc_check', 'M-S': 'trufalse_mc_check', 'MC': 'trufalse_mc_check',
                 'MAT': 'answer_match_check', 'ORD': 'answer_match_check', 'SA': 'answer_match_check',
                 'MSA': 'answer_match_check', 'FIB': 'answer_match_check', 'WR': 'answer_check'}

    # Map each question to its corresponding column using the 'qtype_map' dictionary
    qtype_col = official['Q Type'].map(qtype_map)

    # Assign values to each column in the 'wide_format_df' dataframe using vectorized operations
    wide_format_df['Org Defined ID'] = official['Org Defined ID']
    wide_format_df['Attempt #'] = official['Attempt #']
    wide_format_df['FirstName'] = official['FirstName']
    wide_format_df['LastName'] = official['LastName']
    wide_format_df['Question#'] = official['label']
    wide_format_df['Answer'] = qtype_col

    # Apply relevant mask function to the relevant rows using a boolean mask
    # to avoid applying it to rows that don't need it
    mask = qtype_col == 'trufalse_mc_check'
    mask2 = qtype_col == 'answer_match_check'
    mask3 = qtype_col == 'answer_check'
    wide_format_df.loc[mask, 'Answer'] = official[official['Q Type'].isin(['T/F', 'MC', 'M-S'])]['Answer Match'] \
        .apply(lambda x: trufalse_mc_check(x))
    wide_format_df.loc[mask2, 'Answer'] = official[official['Q Type'].isin(['MAT', 'ORD', 'SA', 'MSA', 'FIB'])] \
        ['Answer Match'].apply(lambda x: answer_match_check(x))
    wide_format_df.loc[mask3, 'Answer'] = official[official['Q Type'] == 'WR']['Answer'] \
        .apply(lambda x: answer_match_check(x))

    # Select the required columns and return the resulting dataframe
    return wide_format_df[['Org Defined ID', 'Attempt #', 'FirstName', 'LastName', 'Question#', 'Answer']]

def qwhole_df_creation(official):
    '''
    Creates dataframe with answers for each whole question(needs to be optimized)
      
    inputs:
    official: the modified_details dataframe
    
    outputs:
    returns dataframe with question whole number and answer columns 
    '''
    question_df = pd.DataFrame(columns=['Org Defined ID', 'Attempt #', 'FirstName', 'LastName',  'Q#', 'Answer'])
    question_df.set_index('Org Defined ID', inplace=True)
    username_values = [value for value in official['Username'].unique()]
    for username in username_values:
        for i, row in official[official['Username'] == username].iterrows():
            if official['Q Type'][i] in ['T/F', 'M-S', 'MC']:
                question_df = pd.concat([question_df,
                                         pd.Series({'Org Defined ID': official['Org Defined ID'][i],
                                                    'Attempt #': official['Attempt #'][i],
                                                    'FirstName': official['FirstName'][i],
                                                    'LastName': official['LastName'][i],
                                                    'Q#': official['newQ#'][i],
                                                    'Answer': trufalse_mc_score(official, i)}).to_frame().T],
                                                    ignore_index=True)
            elif official['Q Type'][i] in ['MAT', 'ORD', 'SA', 'MSA', 'FIB']:
                question_df = pd.concat([question_df,
                                         pd.Series({'Org Defined ID': official['Org Defined ID'][i],
                                                    'Attempt #': official['Attempt #'][i],
                                                    'FirstName': official['FirstName'][i],
                                                    'LastName': official['LastName'][i],
                                                    'Q#': official['newQ#'][i],
                                                    'Answer': official['Answer Match'][i]}).to_frame().T],
                                                    ignore_index=True)
            elif official['Q Type'][i] == 'WR':
                question_df = pd.concat([question_df,
                                         pd.Series({'Org Defined ID': official['Org Defined ID'][i],
                                                    'Attempt #': official['Attempt #'][i],
                                                    'FirstName': official['FirstName'][i],
                                                    'LastName': official['LastName'][i],
                                                    'Q#': official['newQ#'][i],
                                                    'Answer': official['Answer'][i]}).to_frame().T],
                                                    ignore_index=True)

    return question_df[['Org Defined ID', 'Attempt #', 'FirstName', 'LastName', 'Q#', 'Answer']]

def qparts_df_column_list_creation(new_data):
    '''
    Returns a list of question columns for the question parts dataframe(could be integrated into the
    qwhole_df_creation function)
    
    inputs:
    new_data: the question_parts_dataframe
    
    outputs:
    list containing question parts of dataframe for every user except the "answerkey" user
    '''

    temp_columns = []
    q_list = []

    for question in new_data[new_data['Org Defined ID'] == new_data['Org Defined ID'].unique()[1]]['Question#']:
        if question not in q_list:
            q_list.append(question)
            temp_columns.append(str(question))
        elif question in q_list:
            q_list = []
            break

    return temp_columns

def user_details_question_formatting(qparts_df_col_list, question_parts_df):
    '''
    Creates modified qparts dataframe according to the user question format(could be integrated into the
    qwhole_df_creation function)
    
    inputs:
    qparts_df_col_list: list containing question parts of question parts dataframe
    question_parts_df: the question parts dataframe
    
    outputs:
    modified question parts dataframe with question numbers and answers common to every user including the 
    "answerkey" user
    '''

    wide_format_df = pd.DataFrame(columns=['Org Defined ID', 'Attempt #', 'FirstName', 'LastName',
                                           'Question#', 'Answer'])
    id_values = [value for value in question_parts_df['Org Defined ID'].unique()]
    for id in id_values:
        for i, row in question_parts_df[question_parts_df['Org Defined ID'] == id].iterrows():
            if question_parts_df['Question#'][i] in qparts_df_col_list:
                wide_format_df = pd.concat([wide_format_df,
                                            pd.Series({'Org Defined ID': question_parts_df['Org Defined ID'][i],
                                                       'Attempt #': question_parts_df['Attempt #'][i],
                                                       'FirstName': question_parts_df['FirstName'][i],
                                                       'LastName': question_parts_df['LastName'][i],
                                                       'Question#': question_parts_df['Question#'][i],
                                                       'Answer': question_parts_df['Answer'][i]}).to_frame().T],
                                                        ignore_index=True)
    return wide_format_df[['Org Defined ID', 'Attempt #', 'FirstName', 'LastName', 'Question#', 'Answer']]

def question_parts_df_pivot(question_parts_df, col_list):
    '''
    Creates a wide binary format of the question parts dataframe
    
    inputs:
    col_list: list containing question parts of question parts dataframe
    question_parts_df: the question parts dataframe
    
    outputs:
    mod_question_parts_df: pivotted question parts dataframe with question parts column renaming
    '''
    mod_question_parts_df = pd.pivot_table(question_parts_df, index=['Org Defined ID', 'Attempt #', 'FirstName', 'LastName'],
                            values='Answer', columns=['Question#'], aggfunc='first')
    mod_question_parts_df = mod_question_parts_df.reindex(col_list, axis=1)
    mod_question_parts_df.columns = ['Q' + str(i) for i in mod_question_parts_df.columns]
    return mod_question_parts_df

def question_whole_df_pivot(question_whole_df):
    '''
    Creates a wide binary format of the question whole dataframe
    
    inputs:
    question_whole_df: the question whole dataframe
    
    outputs:
    mod_question_df: pivotted question whole dataframe with question whole column renaming
    '''
    mod_question_df = pd.pivot_table(question_whole_df, index=['Org Defined ID', 'Attempt #', 'FirstName', 'LastName'],
                                     values='Answer', columns=['Q#'], aggfunc='first')
    mod_question_df.columns = ['Q' + str(j) for j in mod_question_df.columns]
    return mod_question_df

def dataframe_link(col_list, new_data, q_data):
    '''
    uses Python's pivot_table function to convert data into a wide binary format and formats question columns
    
    inputs:
    col_list: list containing question parts of question parts dataframe
    new_data: the question parts dataframe
    q_data: the question whole dataframe
    
    outputs:
    concatenation of the pivotted question parts dataframe and the question whole dataframe
    '''
    return pd.concat([question_parts_df_pivot(new_data, col_list), question_whole_df_pivot(q_data)], axis=1)

def completeQuiz(attemptdetails, questiondetails, qa_label_key = False):
    '''
    converts csv data into a wide, binary format using functions
    
    inputs:
    attemptdetails: the data that contains user attempts on questions
    questiondetails: the data that contains quiz answers
    qa_label_key: A boolean that allows you to set if you want the question and answer label key outputted along with the final data output. It's default is false (no label key), but true will return the label key as well. 
    
    outputs:
    wide_format_data: the wide, binary formatted dataframe where 0 and 1 represent checked or 
    unchecked for question parts and correct or incorrect answers. For questions other than 
    True/False, MC, or M-S, the dataframe outputs the user answer

    if qa_label_key is true:
        qa_label_df: the label dataframe consisting of new label, question text, and answer text. 
    '''
    user_details, quiz_details = readincsv(attemptdetails, questiondetails)
    mod_user_details = answerKeyOnTop(user_details, quiz_details)
    mod_qorder_user_details = createQuizOrder(mod_user_details, quiz_details)
    #qdict = question_dictionary(mod_qorder_user_details)
    qa_label_data = qa_label_dictionary(mod_qorder_user_details)
    question_parts_df = qparts_df_creation(mod_qorder_user_details)
    question_parts_df_col_list = qparts_df_column_list_creation(question_parts_df)
    question_whole_df = qwhole_df_creation(mod_qorder_user_details)
    wide_format_data = dataframe_link(question_parts_df_col_list, question_parts_df, question_whole_df)
    if qa_label_key == True:
        return wide_format_data, qa_label_data
    else:
        return wide_format_data


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Test case 1 and 2: Looks at whether a value in a column has the actual value or not
assert(x['Q1.01'][2] == 1)
assert(x['Q6.01'][6] == 'Spartan')


#Test case 3: Determines whether an index column is actually in the index as well as a value in a column
assert(x.index.get_level_values(0)[3] in x.index.get_level_values(0)
       and x['Q15.01'][0] == 'My favorite animal is a dog because people spend so much time with them.')

#Test case 4: Determines whether a level value exists or not(Needs work)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
assert(Index(['Key', 'Dec', 'Agusti', 'Sun', 'Patel', 'Ramsey', 'Wolf', 'Berg', 'Nugent', 'Student', 'Student',
              'Student', 'Parks', 'Rau', 'Saini', 'Riggs', 'Peacock'], dtype='object', name='LastName')
       == x.index.get_level_values(3).values.all())
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Test case 5-8: Determines whether a value in an index or column exists based on the assertion
assert(x.index.get_level_values(0)[9] == 'DemoStudent_1897625_63d2d4ac059b3')
assert(x.index.get_level_values(0)[9] == 'DemoStudent_1897625_63d2d4ac059b3' and x['Q10.02'][9] == 'cat')
assert(x.index.get_level_values(0)[9] == 'DemoStudent_1897625_63d2d4ac059b3' and x['Q10.02'][10] == 'doggi')
assert(x.index.get_level_values(1)[2] == 1 and x.index.get_level_values(3)[2] == 'Agusti' and x['Q25.0'][2] == 0)

#Test case 9:Checks for the presence of NaN values
assert(x.isnull().values.any())

#Test case 10: Gives traceback error for non-existant values in either the index column or the actual columns
assert(x.index.get_level_values(2)[11] == 'Demo' and x['Q5.03'][3] == 'Spartan')

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
