from colorsys import rgb_to_hls

def css_to_rgb(color: str) -> (int, int, int):
  """
    Convert a CSS hexadecimal color code to RGB values.

    Args:
    - color (str): A string representing a CSS hexadecimal color code.

    Returns:
    - tuple: A tuple containing the RGB values (red, green, blue) converted from the input color.

    Example:
    >>> css_to_rgb("#FFA500")
    (255, 165, 0)
  """

  # Removing the '#' symbol and converting the hexadecimal color to an integer
  color_int = int(color[1:], 16)

  # Shift 16 bits to the right to get the red value
  red = color_int >> 16

  # Shift 8 bits to the right and apply a mask to get the green value
  green = (color_int >> 8) & 0x00FF

  # Apply a mask to get the blue value
  blue = color_int & 0x0000FF  

  # Return the RGB values as a tuple
  return (red, green, blue)

def css_to_hsl(color: str) -> (float, float, float):
  """
    Convert a CSS hexadecimal color code to HSL values.

    Args:
    - color (str): A string representing a CSS hexadecimal color code.

    Returns:
    - tuple: A tuple containing the HSL values (hue, saturation, lightness) converted from the input color.

    Example:
    >>> css_to_hsl("#FFA500")
    (255, 1, 0)
  """

  # Convert CSS to RGB first
  (r, g, b) = css_to_rgb(value)

  # Convert to hue, lightness, and saturation
  (h, l, s) = rgb_to_hls(r / 255, g / 255, b / 255); 

  # Return the HLS values as a tuple
  return (h, 1, l)

def shade_css_color(color: str, percent: float) -> str:
  """
    Darkens or lightens a CSS color by a certain percentage.

    Args:
    - color (str): The CSS color code in hexadecimal format (e.g., "#RRGGBB").
    - percent (float): The percentage by which the color should be shaded.
                       A negative value darkens the color, and a positive
                       value lightens the color.

    Returns:
    - str: The modified CSS color code after shading.
  """

  # Convert CSS color to RGB
  (r, g, b) = css_to_rgb(color)

  # Define the minimum and maximum values for color components
  min_value = 0
  max_value = 255

  # Determine whether to lighten or darken the color based on the percentage
  target_value = min_value if percent < 0 else max_value
  abs_percent = abs(percent)

  # Calculate new RGB values after shading
  new_r = min(max_value, round((target_value - r) * abs_percent) + r)
  new_g = min(max_value, round((target_value - g) * abs_percent) + g)
  new_b = min(max_value, round((target_value - b) * abs_percent) + b)

  # Format the modified RGB values into a CSS color code and return
  return "#{:02x}{:02x}{:02x}".format(new_r, new_g, new_b)
