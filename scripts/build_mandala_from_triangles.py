from PIL import Image, ImageDraw, ImageOps
import os
import random

# ==== CONFIG ====
output_size = 3000
triangle_angle = 22.5
center = (output_size // 2, output_size // 2)
output_name = "final_mandala_symmetric.png"

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

if len(same_size_jpgs) < 8:
    raise Exception("❌ Not enough .jpgs of same size.")

selected = random.sample(same_size_jpgs, 8)
print("🧩 Using:")
for f in selected:
    print(f"   {f}")

# ==== FUNCTION: CREATE 90° SYMMETRIC QUADRANT ====
def create_quadrant(img):
    img = img.resize((output_size, output_size))

    # Triangle mask
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([0, 0, output_size, output_size], 0, triangle_angle, fill=255)

    triangle = Image.new("RGBA", img.size, (0, 0, 0, 0))
    triangle.paste(img, (0, 0), mask)

    # Mirror horizontally (get 45° wedge)
    wedge45 = ImageOps.mirror(triangle)

    wedge45_full = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wedge45_full.alpha_composite(triangle)
    wedge45_full.alpha_composite(wedge45)

    # Mirror vertically (get 90° quadrant)
    wedge90 = ImageOps.flip(wedge45_full)

    final_quadrant = Image.new("RGBA", img.size, (0, 0, 0, 0))
    final_quadrant.alpha_composite(wedge45_full)
    final_quadrant.alpha_composite(wedge90)

    return final_quadrant

# ==== BUILD FINAL MANDALA ====
mandala = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

for i, fname in enumerate(selected):
    with Image.open(fname) as img:
        quadrant = create_quadrant(img)
        rotated = quadrant.rotate(i * 45, resample=Image.BICUBIC, center=center)
        mandala.alpha_composite(rotated)

# ==== SAVE TRANSPARENT PNG ====
mandala.save(output_name)
print(f"✅ Saved: {output_name}")
