import numpy as np
import pandas as pd
import sys

def validateFormat(df, subjects):
  columns = df.columns.to_list()

  # Check for name and attendance columns
  column_to_check = ["name", "attendance"]
  for column in column_to_check:
    if column not in columns:
      print(f"\nInvalid format. Missing column '{column}'")
      print("Make sure file has correct format: roll_no, name, attendance, <subjects>\n")
      sys.exit(3)
  # Trim whitespace from roll_no, name
    df.index = df.index.str.strip()
    df["name"] = df["name"].str.strip()

  # Check for null roll no
  null_index_df = df[df.index.isna()]
  if null_index_df["name"].count() != 0:
      null_index_df.index = null_index_df.index.fillna("empty")
      print("\nInvalid data. Following rows have empty roll no:\n")
      print(null_index_df.to_string())
      sys.exit(4)
  
  # Check for duplicate roll numbers
  if not df.index.is_unique:
    print("\nInvalid data. The following rows have duplicate roll no:\n")
    print(df[df.index.duplicated()].to_string())
    sys.exit(4)

  # Check if there is atleast one subject column
  if len(subjects) == 0:
    print("\nInvalid format. Should have atleast one subject column")
    print("Make sure file has correct format: roll_no, name, attendance, <subjects>\n")
    sys.exit(3)
  
  # Check data type of attendance, subjects to be numeric
  for column in ["attendance", *subjects]:
    if df[column].dtype not in ["int64", "float64"]:
      print(f"\nInvalid format. Non numeric data in column '{column}'\n")
      sys.exit(3)

  # Check for null values
  null_rows_df = df[df.isna().any(axis=1)]
  if null_rows_df["name"].count() != 0:
    null_rows_df = null_rows_df.astype(str)
    null_rows_df.fillna("empty", inplace=True)
    print("\nInvalid data. Following rows have empty values:\n")
    print(null_rows_df.to_string())
    sys.exit(4)
  

def validateDataRange(df, subjects, max_subject_marks, no_of_lectures):
  # Drop attendance out of range rows
  invalid_attendance_df = df[(df["attendance"] < 0) | (df["attendance"] > no_of_lectures)]
  if invalid_attendance_df["name"].count() != 0:
    print("\nInvalid data. The following rows have attendance out of range:\n")
    print(invalid_attendance_df[["name", "attendance"]].to_string())
    sys.exit(4)
  
  # Drop marks out of range rows
  invalid_marks_df = df[((df[subjects] < 0) | (df[subjects] > max_subject_marks)).any(axis=1)]
  if invalid_marks_df["name"].count() != 0:
    print("\nInvalid data. The following rows have marks out of range:\n")
    print(invalid_marks_df[["name", *subjects]].to_string())
    sys.exit(4)  


if __name__ == "__main__":
  students_df = pd.read_csv("sample-invalid-csv/duplicate-data.csv", index_col="roll_no")
  students_df.index = students_df.index.astype(str)
  validateFormat(students_df)
  validateDataRange(students_df, 100, 100)
  print(students_df)
