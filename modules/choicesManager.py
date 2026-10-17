def displayChoices(choices, heading = None):
  if heading:
    print(headingFormatter(heading))
  count = 1
  for choice in choices:
    print(str(count) + ". " + choice)
    count += 1
  return [str(i) for i in range(1, count)]

def handleChoiceSelection(valid_choices):
  while(True):
    user_choice = input("Enter your choice: ")
    if user_choice in valid_choices:
      return user_choice

def headingFormatter(text):
  padding = 20
  return f"\n{'=' * padding} {text} {'=' * padding}\n"


# Testing the module
if (__name__ == "__main__"):
  valid_choices = displayChoices(["Display record", "Do whatever we want", "Beat everyone up"], "MAIN MENU")
  user_choice = handleChoiceSelection(valid_choices)
  print(f"You chose: {user_choice}")