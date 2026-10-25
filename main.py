import pandas as pd
import sys

from modules import choicesManager as cm, helperFunctions as hf, recordsAnalyzer as ra, dataCleaner as dc


if len(sys.argv) == 1:
  print("Invalid command. Use command: python main.py <Path to your csv file>")
  sys.exit(1)

try:
  students_df = pd.read_csv(sys.argv[1])
except FileNotFoundError:
  print("\nFile not found. Make sure file path is correct.\n")
  sys.exit(2)
except pd.errors.EmptyDataError:
  print("\nEmpty file. Nothing to do.\n")
  sys.exit(2)

students_df = dc.cleanColumnNames(students_df)
students_df = students_df.set_index("roll_no")
# roll_no is used as index. Everything else except name and attendance is treated as a subject.
subjects = [column for column in students_df.columns if column not in ["name", "attendance", "department"]]
# Change roll no data type to object since roll no can be string also and to allow us to compare to it using string
students_df.index = students_df.index.astype("string")
# Validate and clean the file, data
dc.validateFormat(students_df, subjects)

print(hf.headingFormatter("INITIAL SETUP", "-"))
while True:
  max_subject_marks = hf.takeFloatInput("Enter maximum marks of a subject: ")
  passing_marks = hf.takeFloatInput("Enter passing marks of a subject: ")
  no_of_lectures = hf.takeIntInput("Enter number of lectures held (for attendance): ")
  if (no_of_lectures <= 0 or max_subject_marks <= 0 or passing_marks < 0):
    print("\nInvalid value. Values cannot be negative.\n")
    continue
  if (max_subject_marks < passing_marks):
    print("\nPassing marks cannot be greater than maximum subject marks\n")
    continue
  break
# Validate the attendance, marks
dc.validateDataRange(students_df, subjects, max_subject_marks, no_of_lectures)

print(f"\nSuccessfully loaded the csv file. {students_df['name'].count()} records loaded.")

analyzed_df = ra.analyzeStudents(students_df, subjects, max_subject_marks, passing_marks, no_of_lectures)
subject_analysis_df = ra.analyzeSubjects(students_df, subjects, passing_marks)

while True:
  print(hf.headingFormatter("MAIN MENU", "-"))
  valid_choices = cm.displayChoices([
    "View all student records",
    "View analyzed student records",
    "View an individual student report",
    "View class performance summary",
    "View subject-wise analysis",
    "View top performers"
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
      hf.waitEnter()

    case "View analyzed student records":
      print(hf.headingFormatter("ANALYZED STUDENT RECORDS"))
      print(analyzed_df.to_string())
      hf.waitEnter()

    case "View an individual student report":
      print(hf.headingFormatter("STUDENT REPORT"))
      while True:
        input_roll_no = input("Enter student roll no: ").strip()
        if input_roll_no in students_df.index:
          break
        else:
          print("Invalid roll no. Try again.\n")
      print('_' * 30)
      print(f"roll_no        {input_roll_no}")
      cols = ["name"] + (["department"] if "department" in students_df.columns else [])
      print(students_df.loc[input_roll_no, cols].to_string())
      print()
      print("Subject Marks")
      print(students_df.loc[input_roll_no, subjects].to_string())
      print('-' * 30)
      print(analyzed_df.loc[input_roll_no, ["average", "total", "percentage", "grade", "result", "attendance"]].to_string())
      print("_" * 30)
      hf.waitEnter()

    case "View class performance summary":
      class_analysis = ra.analyzeClass(analyzed_df)
      print(hf.headingFormatter("CLASS PERFORMANCE SUMMARY"))
      print(f"""Total students: {class_analysis["total_students"]}
Average Class Percentage: {class_analysis["avg_percentage"]}%
Highest Student Percentage: {class_analysis["highest_percentage"]}%
Lowest Student Percentage: {class_analysis["lowest_percentage"]}%

Students Passed: {class_analysis["no_of_passed"]}
Students Failed: {class_analysis["no_of_failed"]}
Pass Percentage: {class_analysis["pass_percentage"]}%""")
      hf.waitEnter()

    case "View subject-wise analysis":
      print(hf.headingFormatter("SUBJECT-WISE PERFORMANCE"))
      print(subject_analysis_df.to_string())
      print(f"\nSubject with highest average: {subject_analysis_df['average'].idxmax()}")
      print(f"Subject with lowest average: {subject_analysis_df['average'].idxmin()}")
      hf.waitEnter()

    case "View top performers":
      print(hf.headingFormatter("TOP PERFORMERS"))
      print(analyzed_df[["name", "percentage"]].sort_values(by=["percentage"], ascending=False).head(10).to_string())
      hf.waitEnter()