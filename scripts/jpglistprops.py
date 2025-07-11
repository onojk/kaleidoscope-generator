from PIL import Image
import os

folder = "/home/onojk123/Downloads/222222222222222222"
print(f"{'File Name':<45} {'Size (KB)':<10} {'Dimensions':<15} {'Mode':<8}")

for filename in sorted(os.listdir(folder)):
    if filename.lower().endswith(".jpg"):
        path = os.path.join(folder, filename)
        with Image.open(path) as img:
            width, height = img.size
            size_kb = os.path.getsize(path) // 1024
            mode = img.mode
            print(f"{filename:<45} {size_kb:<10} {width}x{height:<10} {mode}")
