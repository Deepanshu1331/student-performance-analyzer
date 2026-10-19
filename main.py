import pandas as pd
import sys

from modules import choicesManager as cm, helperFunctions as hf, recordsAnalyzer as ra


if len(sys.argv) == 1:
  print("Invalid command. Use command: python main.py <Path to your csv file>")
  sys.exit(1)

try:
  students_df = pd.read_csv(sys.argv[1], index_col="roll_no")
except FileNotFoundError:
  print("File not found. Make sure file path is correct.")
  sys.exit(2)

print()
max_subject_marks = hf.takeIntInput("Enter maximum marks of a subject: ")
passing_marks = hf.takeIntInput("Enter passing marks of a subject: ")
no_of_lectures = hf.takeIntInput("Enter number of lectures held (for attendance): ")
# Assuming csv file columns to be roll_no, name, attendance then subjects. Start from 2 cause roll_no is index
subjects = students_df.columns.to_list()[2:]  

analyzed_df = ra.analyzeStudents(students_df, subjects, max_subject_marks, passing_marks, no_of_lectures)

while True:
  print(hf.headingFormatter("MAIN MENU"))
  valid_choices = cm.displayChoices([
    "View all student records",
    "View analyzed student records",
    "View an inidividual student report",
    "View class performance summary",
    "View subject-wise analysis"
  ])
  print("0. Exit\n")
  valid_choices[0] = "Exit"

  user_choice = cm.handleChoiceSelection(valid_choices.keys())
  match valid_choices[user_choice]:
    case "Exit":
      break

    case "View all student records":
      print(hf.headingFormatter("STUDENT RECORDS"))
      print(students_df.to_string())

    case "View analyzed student records":
      print(hf.headingFormatter("ANALYZED STUDENT RECORDS"))
      print(analyzed_df.to_string())

    case "View class performance summary":
      class_analysis = ra.analyzeClass(analyzed_df)
      print(hf.headingFormatter("CLASS PERFORMANCE SUMMARY"))
      print(f"""Total students: {class_analysis["total_students"]}
Class average: {class_analysis["avg_percentage"]}%
Highest Student Percentage: {class_analysis["highest_percentage"]}%
Lowest Student Percentage: {class_analysis["lowest_percentage"]}%

Students Passed: {class_analysis["no_of_passed"]}
Students Failed: {class_analysis["no_of_failed"]}
Pass Percentage: {class_analysis["pass_percentage"]}%""")

    case "View subject-wise analysis":
      print(hf.headingFormatter("SUBJECT-WISE PERFORMANCE"))
      print(ra.analyzeSubjects(students_df, subjects).to_string())