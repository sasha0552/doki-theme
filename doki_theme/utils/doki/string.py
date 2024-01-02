from re import compile, sub
from typing import Dict

def replace_placeholders(input_string: str, replacements: Dict[str, str]) -> str:
  # Initialize the output string with the input string
  output_string = input_string

  # Iterate through each key-value pair in the replacements dictionary
  for pattern, replacement in replacements.items():
    # Use regular expression to substitute the pattern with its replacement in the output string
    output_string = sub(compile(f"&{pattern}&"), replacement, output_string)

  # Return resulting string
  return output_string
