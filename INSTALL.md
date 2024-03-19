Please see the README.md for further information on our project.

# Installations and Dependencies

Please see our 'Reports' directory for conda installation instructions as well as requirements and limitations of our software. 

## Importing Our Library

Bring our library into your code or notebook by using the command ```from src.d2lapi import``` then type what directories / modules you'd like to use. As a note, this may change depending on what folder you are working in!  

The options are as follows:
1. Final_Quiz: functions to convert quiz data, import using ```from src.d2lapi import Final_Quiz```
2. Final_Survey: functions to convert survey data, import using ```from src.d2lapi import Final_Survey```
3. Visualization_Bar: functions to create distribution visualization, import using ```from src.d2lapi import Visualization_Bar```
4. D2L_Widgets: functions to help with widgets, import using ```from src.d2lapi import D2L_Widgets```


## Downloading Our PyPi Library
As an alternative to downloading our entire repository you may also simply type ```pip install d2lapi``` into a terminal and enter.

Bring our library into your code or notebook by using the command ```from d2lapi import``` then type what directories / modules you'd like to use. 

The options are as follows:
1. Final_Quiz: functions to convert quiz data, import using ```from d2lapi import Final_Quiz```
2. Final_Survey: functions to convert survey data, import using ```from d2lapi import Final_Survey```
3. Visualization_Bar: functions to create distribution visualization, import using ```from d2lapi import Visualization_Bar```
4. D2L_Widgets: functions to help with widgets, import using ```from d2lapi import D2L_Widgets```


As a note, every time you use functions from our library, you will have to reference the corresponding directory like so: ```Final_Quiz.completeQuiz()```. 
The syntax is: ```<module>.<function>```

## Installing Jupyter Notebook 

1. Open a command line environment. For Mac users open ‘Terminal’. For Windows users open ‘Command Prompt’ 

2. Install the latest python3 in your local system: https://www.python.org/downloads/  

3. Verify installation was completed by running “python --version” in the command line.   
    PIP should be a prerequisite  and should be installed on your system. To verify that PIP is installed type “pip --version” in the command line. 

4. To install Jupyter Notebook run “pip install notebook”. 

5. On your local system, to run a Jupyter Notebook environment type “jupyter notebook” in the command line. 

## Environment

We have a provided an environment.yml file for setting up a conda environment to work with our repository.

Please use the following commands to use it:

```conda env create --prefix ./envs --file environment.yml```

Then

```conda activate ./envs```

# D2L

*The pre-requisite for all D2L related tutorials is that you have certain administrative roles. (At least course editor). You can check your role on the class list section of D2L. 

Click [this link](https://mediaspace.msu.edu/media/Getting+D2L+Data+Output+Tutorial/1_i9pbey6y) for a video tutorial about getting data from D2L. 

## Getting the quiz attempt csv from D2L: 

1. Login to D2L and go to course page  

2. At the top of the screen the drop-down “Assignments” and navigate to “Quizzes” 

3. Select the carrot (V) next to the desired quiz and select “Grade”.  
    You should be redirected to a page titled “Grade Quiz – [Quiz Name]” 

4. On this new page you should check all (desired) students then select export as csv.  

5. Save the file in our API. 



## Getting the survey attempt csv from D2l: 

*To get a report on the surveys steps 4-7 must be done before the respondents respond. 

1. Login D2l and go to the course page. 

2. Go to “Assessment” and click the “Surveys”. 

3. Find the survey you desire to export and to go to the survey.  

4. Go to “Reports Setup”. 

5. Add new report by clicking “Add Report”. 

6. Name it and Select  “Individual Attempts”, save it.  

7. Return to “Surveys”. 

8. Select “Reports”. 

9. Go to the report just added. 

10. Select Generate CSV. 


## Getting the answer key from D2L: 

1. Log into D2L first and select the course you would like 

2. Under the Assessments drop-down menu, select Quizzes 

3. Select Statistics from the carrot symbol next to Final Quiz 

4. Finally, select Question Details and click the “Export to CSV” button 


# Example Data

## Getting Example Data: 

To try out the API, without exporting data from D2L, we have provided example data files to run through the Jupyter Notebooks, such as 'Widget-Based_GUI.ipynb' and 'Bar_Visualization.ipynb'. They are located in the repository under 'DataFiles' and titled 'ExampleData_QuizAttemptDetails.csv', 'ExampleData_AnswerKey.csv', and 'ExampleData_Survey.csv'. For ease of use, please ensure that these data files are located in the same directory as the Jupyter Notebook on your computer.  


## Incorporating the Example Data into the Notebook: 

1. Navigate to the Jupyter Notebook you’d like to run. 

2. Replace the name of the .csv files needed in code with your example files. Files with “Attempt Details” in the name should be replaced with 'ExampleData_QuizAttemptDetails.csv'. Files with “Question Details” in the name should be replaced with “'ExampleData_AnswerKey.csv', and survey related data should be replaces with 'ExampleData_Survey.csv'. You can also use the provided widgets to help you bring in example data.


## Inputs and Outputs

Information on inputs and outputs of the software can be found in the 'UsageRequirementsLimitations.md' file under the 'Reports' directory, as well as function definitions, and instructions included in the various GUIs or usage examples. 