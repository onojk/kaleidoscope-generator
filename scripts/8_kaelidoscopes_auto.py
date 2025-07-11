from PIL import Image, ImageDraw, ImageOps
import os
import random

# ==== CONFIG ====
output_size = 3000
triangle_angle = 22.5
center = (output_size // 2, output_size // 2)

# ==== STEP 1: GET 8 JPGs OF SAME SIZE ====
all_jpgs = [f for f in os.listdir('.') if f.lower().endswith('.jpg')]

if len(all_jpgs) == 0:
    raise Exception("No .jpg images found.")

# Use the first image to get the size
with Image.open(all_jpgs[0]) as test_img:
    base_size = test_img.size

same_size_jpgs = []
for f in all_jpgs:
    try:
        with Image.open(f) as img:
            if img.size == base_size:
                same_size_jpgs.append(f)
    except:
        continue

if len(same_size_jpgs) < 8:
    raise Exception("❌ Not enough matching-size .jpg files (need 8).")

selected = random.sample(same_size_jpgs, 8)
print("📷 Using these 8 base images:")
for f in selected:
    print(f"   {f}")

# ==== FUNCTION TO MAKE 45° WEDGE ====
def create_45_degree_wedge(img):
    img = img.resize((output_size, output_size))

    # 22.5° triangle mask
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([0, 0, output_size, output_size], 0, triangle_angle, fill=255)

    triangle = Image.new("RGBA", img.size, (0, 0, 0, 0))
    triangle.paste(img, (0, 0), mask)

    # Mirror horizontally to get full 45° wedge
    mirrored = ImageOps.mirror(triangle)

    wedge = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wedge.alpha_composite(triangle)
    wedge.alpha_composite(mirrored)

    return wedge

# ==== LOOP: GENERATE 8 MANDALAS ====
for idx, fname in enumerate(selected):
    print(f"🔄 Creating mandala #{idx+1} from {fname}")
    with Image.open(fname) as img:
        wedge = create_45_degree_wedge(img)

        # Start new mandala canvas
        mandala = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))

        # Rotate and place 8 wedges
        for i in range(8):
            rotated = wedge.rotate(i * 45, resample=Image.BICUBIC, center=center)
            mandala.alpha_composite(rotated)

        out_name = f"mandala_{idx+1:02d}_from_{os.path.splitext(fname)[0]}.png"
        mandala.save(out_name)
        print(f"✅ Saved: {out_name}")
