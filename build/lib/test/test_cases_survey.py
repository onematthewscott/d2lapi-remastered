import pytest
import pandas as pd
import numpy as np
from src import Final_Survey

def test_trufalse_mc_check():
    assert Final_Survey.trufalse_mc_check(1.000) == 1
    assert Final_Survey.trufalse_mc_check(0.000) == 0
    assert Final_Survey.trufalse_mc_check(0.500) == 0.500
    assert Final_Survey.trufalse_mc_check(1.001) == 1.001
def test_nullRowChecker():
    user_arr = []

    non_null_input = 1
    non_null_output = Final_Survey.nullRowChecker(non_null_input, user_arr)
    assert np.isnan(non_null_output), "Expected np.nan for non-null input"
    assert user_arr == [1], "Expected user_arr to have the non-null input value"

    null_input = np.nan
    null_output = Final_Survey.nullRowChecker(null_input, user_arr)
    assert null_output == 1, "Expected the last non-null value in user_arr for null input"
    assert user_arr == [1], "Expected user_arr to remain unchanged for null input"

    
def test_answer_match_check():
    assert Final_Survey.answer_match_check("A") == "A"
    assert Final_Survey.answer_match_check("test") == "test"
    assert Final_Survey.answer_match_check(42) == 42
    assert Final_Survey.answer_match_check(None) == None
    assert Final_Survey.answer_match_check(0) == 0

def test_answer_check():
    assert Final_Survey.answer_check("check") == "check"
    assert Final_Survey.answer_check("wrong") != "true"
    assert Final_Survey.answer_check(11.6) !=11.9
    assert Final_Survey.answer_check(8.11) == 8.11
    assert Final_Survey.answer_check(0) != 1
    
def test_question_df_creation():
    data = {
        "User": [1, 1, 2, 2],
        "Q Type": ["T/F", "MC", "SA", "WR"],
        "# Responses": [1.000, 0.000, np.nan, np.nan],
        "Answer Match": [np.nan, np.nan, "Answer1", "Answer2"],
        "Answer": [np.nan, np.nan, np.nan, "Answer3"],
        "label": ["Q1", "Q2", "Q1", "Q2"],
    }
    df = pd.DataFrame(data)
    result = Final_Survey.question_df_creation(df)

    expected_data = {
        "User": [1, 1, 2, 2],
        "Question #": ["Q1", "Q2", "Q1", "Q2"],
        "Answer": [1, 0, "Answer1", "Answer3"],
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result, expected_df)

def test_question_df_column_list_creation():
    data = {
        "User": [1, 1, 1, 2, 2, 2],
        "Question #": ["Q1", "Q2", "Q3", "Q1", "Q2", "Q3"],
        "Answer": [1, 0, "Answer1", 1, 0, "Answer2"],
    }
    df = pd.DataFrame(data)
    result = Final_Survey.question_df_column_list_creation(df)

    expected_result = ["Q1", "Q2", "Q3"]

    assert result == expected_result









