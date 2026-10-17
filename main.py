import pandas as pd
import sys

from modules import choicesManager as cm

if len(sys.argv) == 1:
  print("Invalid command. Use command: python main.py <Path to your csv file>")
  sys.exit(1)

try:
  students_df = pd.read_csv(sys.argv[1], index_col="roll_no")
except FileNotFoundError:
  print("File not found. Make sure file path is correct.")

valid_choices = cm.displayChoices([
  "View all student records",
  "View an inidividual student report",
  "View class performance summary",
], heading = "MAIN MENU")
print("0. Exit\n")
valid_choices.append("0")

user_choice = cm.handleChoiceSelection(valid_choices)