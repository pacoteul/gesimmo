from PIL import Image
import sys

def make_transparent(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()

        # Assuming the background is the color of the top-left pixel
        bg_color = datas[0]
        # Let's check if it's mostly white or black
        is_bg_white = bg_color[0] > 128

        newData = []
        for item in datas:
            # Check if pixel is close to background color
            # Allow some tolerance for jpeg artifacts
            if is_bg_white:
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            else:
                if item[0] < 50 and item[1] < 50 and item[2] < 50:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
        
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Successfully processed {input_path} -> {output_path}")
        print(f"Background was assumed to be {'white' if is_bg_white else 'black'}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    make_transparent("logo.jpg", "logo.png")
