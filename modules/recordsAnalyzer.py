import numpy as np
import pandas as pd

def analyzeStudents(df, subjects, max_subject_marks, passing_marks, no_of_lectures):
  analysis_df = pd.DataFrame(df["name"], index=df.index)
  analysis_df["average"] = df[subjects].mean(axis=1)
  analysis_df["total"] = df[subjects].sum(axis = 1)
  analysis_df["percentage"] = analysis_df["total"] / (max_subject_marks * len(subjects)) * 100
  analysis_df["grade"] = assignGrade(analysis_df["percentage"])
  analysis_df["result"] = checkPass(df[subjects], subjects, passing_marks)
  analysis_df["attendance"] = df["attendance"] / no_of_lectures * 100
  return analysis_df

def assignGrade(percentage_df):
  grades = ["A+", 'A', 'B', 'C', 'D', 'E']
  score_condn = [ percentage_df.between(90, 100, "both"), percentage_df.between(80, 90, "left"),
                  percentage_df.between(70, 80, "left"), percentage_df.between(60, 70, "left"),
                  percentage_df.between(50, 60, "left"), percentage_df.between(40, 50, "left"), ]
  grade_arr = np.select(score_condn, grades, default='F')
  return grade_arr

def checkPass(subjects_df, subjects, passing_marks):
  result_arr = None
  for subject in subjects:
    result_arr = np.where(subjects_df[subject] > passing_marks, "pass", "fail")
  return result_arr


def analyzeClass(analyzed_df):
  class_analysis = {}
  class_analysis["total_students"] = analyzed_df["name"].count()
  class_analysis["avg_percentage"] = analyzed_df["percentage"].mean()
  class_analysis["highest_percentage"] = analyzed_df["percentage"].max()
  class_analysis["lowest_percentage"] = analyzed_df["percentage"].min()
  class_analysis["no_of_passed"] = analyzed_df[analyzed_df["result"] == "pass"]["name"].count()
  class_analysis["no_of_failed"] = class_analysis["total_students"] - class_analysis["no_of_passed"]
  class_analysis["pass_percentage"] = (class_analysis["no_of_passed"] / class_analysis["total_students"]) * 100
  return class_analysis

def analyzeSubjects(df, subjects):
  subject_analysis_df = pd.DataFrame(columns=["average", "highest", "lowest"])
  for subject in subjects:
    subject_df = pd.DataFrame([{"average": df[subject].mean(), "highest": df[subject].max(), "lowest": df[subject].min()}], 
                              index=[subject])
    subject_analysis_df = pd.concat([subject_analysis_df, subject_df])
  return subject_analysis_df

if __name__ == "__main__":
  df = pd.read_csv("./students-sample.csv", index_col="roll_no")
  print(df)
  subjects = df.columns.to_list()[2:]
  analyzed_df = analyzeStudents(df, subjects, 100, 40, 100)
  print(analyzed_df)
  class_analysis = analyzeClass(analyzed_df)
  print(class_analysis.items())
  print(analyzeSubjects(df, subjects))