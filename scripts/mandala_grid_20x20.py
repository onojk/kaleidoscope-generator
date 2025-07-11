from PIL import Image
import os
import random

# ==== CONFIG ====
grid_size = 20
scale_percent = 5
output_file = "mandala_grid_20x20.png"

# ==== STEP 1: GET .JPG FILES ====
jpgs = [f for f in os.listdir('.') if f.lower().endswith('.jpg')]
if not jpgs:
    raise Exception("❌ No .jpg files found in this directory.")

# ==== STEP 2: FILTER BY DIMENSION RANGE ====
# Use first image as reference
with Image.open(jpgs[0]) as ref_img:
    w_ref, h_ref = ref_img.size

tolerance = 0.10  # ±10%
w_min, w_max = int(w_ref * (1 - tolerance)), int(w_ref * (1 + tolerance))
h_min, h_max = int(h_ref * (1 - tolerance)), int(h_ref * (1 + tolerance))

valid_pool = []
for f in jpgs:
    try:
        with Image.open(f) as img:
            w, h = img.size
            if w_min <= w <= w_max and h_min <= h <= h_max:
                valid_pool.append(f)
    except:
        continue

if not valid_pool:
    raise Exception("❌ No .jpgs within ±10% size tolerance.")

print(f"📸 Using {len(valid_pool)} image(s) matching size ±10% of reference ({w_ref}x{h_ref})")

# ==== STEP 3: COMPUTE TILE SIZE ====
tile_w = int(w_ref * scale_percent / 100)
tile_h = int(h_ref * scale_percent / 100)
print(f"🧱 Tile size: {tile_w}x{tile_h} pixels")

# ==== STEP 4: CREATE CANVAS ====
canvas = Image.new("RGB", (tile_w * grid_size, tile_h * grid_size))

# ==== STEP 5: BUILD GRID ====
for y in range(grid_size):
    for x in range(grid_size):
        fname = random.choice(valid_pool)
        with Image.open(fname) as img:
            img_resized = img.resize((tile_w, tile_h), resample=Image.LANCZOS)
            canvas.paste(img_resized, (x * tile_w, y * tile_h))
            print(f"📍 Placed: {fname} → ({x},{y})")

# ==== STEP 6: SAVE ====
canvas.save(output_file)
print(f"\n✅ Saved final image: {output_file}")
