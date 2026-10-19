def headingFormatter(text, symbol="="):
  padded_length = 80
  padding_each_side = (padded_length - len(text)) // 2
  return f"\n{symbol * padding_each_side} {text} {symbol * padding_each_side}\n"

def takeIntInput(text):
  while True:
    user_input = input(text)
    try:
      return int(user_input)
    except ValueError:
      pass

def waitEnter():
  input("\nPress enter to go back to main menu: ")