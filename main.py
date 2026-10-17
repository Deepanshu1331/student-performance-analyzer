import pandas as pd
import sys

if len(sys.argv) == 1:
  print("Invalid command. Use command: python main.py <Path to your csv file>")
  sys.exit(1)


try:
  students_df = pd.read_csv(sys.argv[1], index_col="roll_no")
  print(students_df)
except FileNotFoundError:
  print("File not found. Make sure file path is correct.")

