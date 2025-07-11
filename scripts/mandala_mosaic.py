from PIL import Image, ImageDraw, ImageOps
import os
import math
import random

# ==== CONFIG ====
image_folder = "."         # Folder of source JPGs
output_size = 3000         # Final output canvas size
wedge_angle = 45           # Total angle of each mirrored wedge
half_angle = wedge_angle / 2  # 22.5°
num_wedges = 8
overlap = 1.0              # Prevents gaps between wedges

# ==== LOAD IMAGES ====
filenames = sorted([f for f in os.listdir(image_folder) if f.endswith(".jpg")])
selected_images = random.sample(filenames, num_wedges)  # 8 unique patterns
images = [Image.open(os.path.join(image_folder, f)).resize((output_size, output_size)) for f in selected_images]

# ==== OUTPUT SETUP ====
output = Image.new("RGB", (output_size, output_size), (255, 255, 255))
center = (output_size // 2, output_size // 2)

# ==== CREATE MIRRORED WEDGE ====
def create_mirrored_wedge(img):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([0, 0, img.width, img.height],
                  0 - overlap, half_angle + overlap, fill=255)

    base = Image.new("RGBA", img.size)
    base.paste(img, (0, 0), mask)

    mirrored = ImageOps.mirror(base)
    combined = Image.new("RGBA", img.size, (0, 0, 0, 0))
    combined.alpha_composite(base)
    combined.alpha_composite(mirrored)
    return combined

# ==== BUILD THE FULL KALEIDOSCOPE ====
for i, img in enumerate(images):
    wedge = create_mirrored_wedge(img)
    angle = i * wedge_angle
    rotated = wedge.rotate(-angle, resample=Image.BICUBIC, center=center)
    output.paste(rotated.convert("RGB"), (0, 0), rotated.split()[3])

# ==== CIRCULAR CROP ====
mask = Image.new("L", (output_size, output_size), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse([0, 0, output_size, output_size], fill=255)
output.putalpha(mask)
output = output.convert("RGB")  # remove alpha for JPG

# ==== SAVE ====
output.save("kaleidoscope_mandala.jpg")
print("✅ Saved: kaleidoscope_mandala.jpg")
