import tkinter as tk
import pandas as pd
from tkinter.filedialog import askopenfile, askopenfiles, asksaveasfile
from tkinter import ttk
from src.d2lapi import Final_Quiz, Final_Survey
#pip install ...
#from D2L import d2l

root = tk.Tk()
root.title('D2L Converter')

#include icon for GUI    
img = tk.Image("photo",file="./D2L_Data_Converter_Logo.png")
root.iconphoto(True, img) # you may also want to try this.
root.tk.call('wm','iconphoto', root._w, img)

intro = tk.Label(root,text='Welcome to D2L Data Converter!',pady=10)
intro.pack()
side_note = tk.Label(root,text='Use the .csv files from D2L for reformatting.',pady=10)
side_note.pack()

#include image in the root framework
frame = tk.Frame(root)
frame.pack()

img2 = tk.PhotoImage(file = './D2L_Data_Converter_Logo.png')
img2 = img2.zoom(25)
img2 = img2.subsample(32)
label = tk.Label(frame, image = img2)
label.pack()

tabControl = ttk.Notebook(root)
tabControl.pack(pady=15)

quiz_tab = ttk.Frame(tabControl, width=500, height=500)
survey_tab = ttk.Frame(tabControl, width=500, height=500)

quiz_tab.pack(fill="both",expand=1)
survey_tab.pack(fill="both",expand=1)

tabControl.add(quiz_tab, text="Quiz Tab")
tabControl.add(survey_tab, text="Survey Tab")

def openfiles():
  browse_text1.set("Loading...")
  files = askopenfiles(parent=root, mode='r', title="Choose files.", filetypes=[("CSV", "*.csv")])
  if files is not None:
    #print(Final_Quiz.completeQuiz(files[0].name, files[1].name))
    quiz_res,quiz_label = Final_Quiz.completeQuiz(files[0].name, files[1].name, qa_label_key=True)
    final_quiz = asksaveasfile(title='Save reformatted quiz data',defaultextension='csv',filetypes=[("csv file",".csv"),("Excel file",".xlsx")])
    quiz_res.to_csv(final_quiz)
    final_q_label = asksaveasfile(title='Save quiz question & answer label key',defaultextension='csv',filetypes=[("csv file",".csv"),("Excel file",".xlsx")])
    quiz_label.to_csv(final_q_label)
    final_quiz.close()
    print('Files were sucessfully downloaded.')
  else:
    print('File was not selected or download was not successful.')
  return()

def openfile():
  browse_text2.set("Loading...")
  file = askopenfile(parent=root, mode='r', title="Choose a file.", filetypes=[("CSV", "*.csv")])
  if file is not None:
    #print(Final_Survey.completeSurvey(file.name))
    survey_res,survey_label = Final_Survey.completeSurvey(file.name,qa_label_key=True)
    final_survey = asksaveasfile(title='Save reformatted survey data',defaultextension='csv',filetypes=[("csv file",".csv"),("Excel file",".xlsx")])
    survey_res.to_csv(final_survey)
    final_s_label = asksaveasfile(title='Save survey question & answer label key',defaultextension='csv',filetypes=[("csv file",".csv"),("Excel file",".xlsx")])
    survey_label.to_csv(final_s_label)
    final_survey.close()
    print('Files were successfully downloaded.')
  else:
    print('File was not selected or download was not successful.') 
  return()

browse_text1 = tk.StringVar()  # Dealing with quiz data
browse_text1.set("Select quiz data files (QuestionDetail.csv and AttemptDetail.csv)")
browse_text2 = tk.StringVar()  # Dealing with survey data
browse_text2.set("Select survey data file")

browse_button1 = tk.Button(quiz_tab,textvariable=browse_text1,
 command=lambda:openfiles(),fg='#20bebe')
browse_button2 = tk.Button(survey_tab,textvariable=browse_text2, command=lambda:openfile())

download_text = tk.StringVar()
download_text.set("Download reformatted csv file")

button_quit1 = tk.Button(quiz_tab,text='Exit Program',command=root.quit, fg='#369110')
button_quit2 = tk.Button(survey_tab,text='Exit Program',command=root.quit, fg='#369110')

quiz_instruction1 = tk.Label(quiz_tab,text='1. Click on Select quiz data files button to import files.',pady=5)
quiz_instruction2 = tk.Label(quiz_tab,text='  Note: Provide two quiz files from D2L (QuestionDetail.csv and AttemptDetail.csv)',pady=5)
quiz_instruction3 = tk.Label(quiz_tab,text='2. After submitting files, save converted quiz data to desired location on your system.',pady=5)
quiz_instruction4 = tk.Label(quiz_tab,text='3. Save the quiz question and answer key to match reformatted data to questions from original quiz.',pady=5)
quiz_instruction1.pack()
quiz_instruction2.pack()
quiz_instruction3.pack()
quiz_instruction4.pack()

survey_instruction1 = tk.Label(survey_tab,text='1. Click on Select survey data file button to import files.',pady=5)
survey_instruction2 = tk.Label(survey_tab,text='Note: Provide survey file from D2L (AttemptDetail.csv)',pady=5)
survey_instruction3 = tk.Label(survey_tab,text='2. After submitting files, save converted survey data to desired location on your system.',pady=5)
survey_instruction4 = tk.Label(survey_tab,text='* Must be limited to 1 attempt per user! Having multiple attempts will result in improper formatting.',pady=5)
survey_instruction5 = tk.Label(survey_tab,text='3. Save the survey question and answer key to match reformatted data to questions from original survey.',pady=5)
survey_instruction1.pack()
survey_instruction2.pack()
survey_instruction3.pack()
survey_instruction4.pack()
survey_instruction5.pack()

browse_button1.pack()
browse_button2.pack()
button_quit1.pack()
button_quit2.pack()
root.mainloop()

