from re import Pattern, sub
from typing import List, Tuple

def replace_placeholders(input_string: str, replacements: List[Tuple[Pattern, str]]) -> str:
  # Initialize the output string with the input string
  output_string = input_string

  # Iterate through each key-value pair in the replacements dictionary
  for pattern, replacement in replacements:
    # Use regular expression to substitute the pattern with its replacement in the output string
    output_string = sub(pattern, replacement, output_string)

  # Return resulting string
  return output_string
