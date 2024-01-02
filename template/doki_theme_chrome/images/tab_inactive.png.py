from io import BytesIO
from PIL import Image

def render() -> bytes:
  # Convert CSS color to RGB
  (hr, hg, hb) = css_to_rgb(manifest["colors"]["baseBackground"])

  # Create a new RGBA image
  image = Image.new("RGBA", (300, 120))

  # Fill the top 50 rows with the highlight color
  for i in range(50):
    for j in range(300):
      image.putpixel((j, i), (hr, hg, hb, 255))

  # Save the image to a bytes IO stream
  img_byte_arr = BytesIO()
  image.save(img_byte_arr, format="PNG")

  # Return the image data as bytes
  return img_byte_arr.getvalue()
