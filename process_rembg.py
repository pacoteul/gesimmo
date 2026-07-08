from rembg import remove
from PIL import Image

try:
    input_path = 'logo.jpg'
    output_path = 'logo.png'

    input_img = Image.open(input_path)
    output_img = remove(input_img)
    output_img.save(output_path)
    print(f"Successfully used rembg to process {input_path} -> {output_path}")
except Exception as e:
    print(f"Error: {e}")
