import pytest
import pandas as pd
import numpy as np
#from Final_Quiz import createQuizOrder,trufalse_mc_check,answer_match_check,answer_check,trufalse_mc_score
from src import Final_Quiz

def test_createQuizOrder():
    user_attempt = pd.DataFrame({
        "Q Text": ["Q1", "Q2", "Q3"],
        "Username": ["user1", "user1", "user1"],
        "Attempt #": [1, 1, 1]
    })

    quiz_answer = pd.DataFrame({
        "Q Text": ["Q1", "Q2", "Q3"]
    })

    expected_output = pd.DataFrame({
        "Q Text": ["Q1", "Q2", "Q3"],
        "Username": ["user1", "user1", "user1"],
        "Attempt #": [1, 1, 1],
        "newQ#": [1, 2, 3],
        "label": ["11", "21", "31"]
    })

    result = Final_Quiz.createQuizOrder(user_attempt, quiz_answer)
    pd.testing.assert_frame_equal(result, expected_output)
    
def test_trufalse_mc_check():
    assert Final_Quiz.trufalse_mc_check("Checked") == 1
    assert Final_Quiz.trufalse_mc_check("Unchecked") == 0
    assert Final_Quiz.trufalse_mc_check("Checked") !=0
    assert Final_Quiz.trufalse_mc_check("Unchecked" )!=1

def test_answer_match_check():
    assert Final_Quiz.answer_match_check("A") == "A"
    assert Final_Quiz.answer_match_check("test") == "test"
    assert Final_Quiz.answer_match_check(42) == 42
    assert Final_Quiz.answer_match_check(None) == None
    assert Final_Quiz.answer_match_check(0) == 0

def test_answer_check():
    assert Final_Quiz.answer_check("check") == "check"
    assert Final_Quiz.answer_check("wrong") != "true"
    assert Final_Quiz.answer_check(11.6) !=11.9
    assert Final_Quiz.answer_check(8.11) == 8.11
    assert Final_Quiz.answer_check(0) != 1
    
def test_trufalse_mc_score():
    user_df = pd.DataFrame({
        "Score": [3],
        "Out Of": [5]
    })

    idx = 0
    expected_output = 0
    result = Final_Quiz.trufalse_mc_score(user_df, idx)
    assert result == expected_output
    #'score' column is less than 'out of' column
    
    user_df = pd.DataFrame({
        "Score": [5],
        "Out Of": [5]
    })

    idx = 0
    expected_output = 1
    result = Final_Quiz.trufalse_mc_score(user_df, idx)
    assert result == expected_output
    #'score' column is equal to 'out of' column
    
    user_df = pd.DataFrame({
        "Score": [7],
        "Out Of": [5]
    })

    idx = 0
    expected_output = 1
    result = Final_Quiz.trufalse_mc_score(user_df, idx)
    assert result == expected_output
    #'score' column is greater than 'out of' column























