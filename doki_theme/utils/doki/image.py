from io import BytesIO
from PIL import Image

from utils.color import css_to_rgb

def build_active_tab_image(highlight_color, accent_color):
  # Convert CSS colors to RGB
  (hr, hg, hb) = css_to_rgb(highlight_color)
  (ar, ag, ab) = css_to_rgb(accent_color)

  # Create a new RGBA image
  image = Image.new("RGBA", (300, 120))

  # Fill the top 48 rows with the highlight color
  for i in range(48):
    for j in range(300):
      image.putpixel((j, i), (hr, hg, hb, 255))

  # Fill the bottom 2 rows with the accent color
  for i in range(2):
    for j in range(300):
      image.putpixel((j, i + 48), (ar, ag, ab, 255))

  # Save the image to a bytes IO stream
  img_byte_arr = BytesIO()
  image.save(img_byte_arr, format="PNG")

  # Return the image data in bytes format
  return img_byte_arr.getvalue()

def build_inactive_tab_image(highlight_color):
  # Convert CSS color to RGB
  (hr, hg, hb) = css_to_rgb(highlight_color)

  # Create a new RGBA image
  image = Image.new("RGBA", (300, 120))

  # Fill the top 50 rows with the highlight color
  for i in range(50):
    for j in range(300):
      image.putpixel((j, i), (hr, hg, hb, 255))

  # Save the image to a bytes IO stream
  img_byte_arr = BytesIO()
  image.save(img_byte_arr, format="PNG")
    
  # Return the image data in bytes format
  return img_byte_arr.getvalue()
