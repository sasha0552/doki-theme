from io import BytesIO
from PIL import Image

def render() -> bytes:
  # Convert CSS colors to RGB
  (hr, hg, hb) = css_to_rgb(manifest["colors"]["highlightColor"])
  (ar, ag, ab) = css_to_rgb(manifest["colors"]["accentColor"])

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

  # Return the image data as bytes
  return img_byte_arr.getvalue()
