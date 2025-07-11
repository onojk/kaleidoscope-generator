from PIL import Image, ImageDraw, ImageOps
import os
import random

# ==== CONFIG ====
output_size = 3000
triangle_angle = 22.5
center = (output_size // 2, output_size // 2)
output_name = "mandala_single_sample.png"

# ==== STEP 1: FILTER JPGs BY SIZE ====
all_jpgs = [f for f in os.listdir('.') if f.lower().endswith('.jpg')]

# Use the first to get base size
base_img = Image.open(all_jpgs[0])
base_size = base_img.size
base_img.close()

same_size_jpgs = []
for f in all_jpgs:
    try:
        with Image.open(f) as img:
            if img.size == base_size:
                same_size_jpgs.append(f)
    except:
        continue

if len(same_size_jpgs) == 0:
    raise Exception("❌ No .jpgs of matching size found.")

# Choose ONE image for full mandala
selected = random.choice(same_size_jpgs)
print(f"🌌 Using single image for full mandala: {selected}")

# ==== FUNCTION: CREATE 45° SYMMETRIC WEDGE ====
def create_symmetric_wedge(img):
    img = img.resize((output_size, output_size))

    # Create triangle mask for 22.5°
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([0, 0, output_size, output_size], 0, triangle_angle, fill=255)

    triangle = Image.new("RGBA", img.size, (0, 0, 0, 0))
    triangle.paste(img, (0, 0), mask)

    # Create mirrored pair (horizontal flip)
    mirrored = ImageOps.mirror(triangle)

    # Composite to form 45° wedge
    wedge = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wedge.alpha_composite(triangle)
    wedge.alpha_composite(mirrored)

    return wedge

# ==== BUILD FINAL MANDALA ====
mandala = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

with Image.open(selected) as img:
    wedge = create_symmetric_wedge(img)

    for i in range(8):
        rotated = wedge.rotate(i * 45, resample=Image.BICUBIC, center=center)
        mandala.alpha_composite(rotated)

# ==== SAVE OUTPUT ====
mandala.save(output_name)
print(f"✅ Saved: {output_name}")
