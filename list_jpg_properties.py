import os
from PIL import Image

SOURCE_DIR = "source_images"

def list_image_properties(directory):
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith(".jpg"):
            path = os.path.join(directory, filename)
            try:
                with Image.open(path) as img:
                    print(f"🖼️ {filename}")
                    print(f"   - Format: {img.format}")
                    print(f"   - Size: {img.size[0]}x{img.size[1]} pixels")
                    print(f"   - Mode: {img.mode}")
                    print()
            except Exception as e:
                print(f"⚠️ Could not read {filename}: {e}")

if __name__ == "__main__":
    list_image_properties(SOURCE_DIR)
