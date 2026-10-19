from modules import helperFunctions as hf

def displayChoices(choices):
  count = 1
  for choice in choices:
    print(str(count) + ". " + choice)
    count += 1
  return {i:choices[i - 1] for i in range(1, count)}

def handleChoiceSelection(valid_choices):
  while(True):
    user_choice = hf.takeIntInput("Enter your choice: ")
    if user_choice in valid_choices:
      return user_choice


# Testing the module
# Run modules as python -m modules.choicesManager so that imports resolve correctly
if __name__ == "__main__":
  valid_choices = displayChoices(["Display record", "Do whatever we want", "Beat everyone up"])
  user_choice = handleChoiceSelection(valid_choices)
  print(f"You chose: {user_choice}")