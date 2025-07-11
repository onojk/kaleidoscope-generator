import os
import random
from PIL import Image, ImageOps

# === Settings ===
SOURCE_DIR = "source_images"         # Directory with 800x800 JPEGs
OUTPUT_DIR = "generated_grids"       # Where output mandala grids go
GRID_SIZE = 8                        # 8x8 tiles per grid
NUM_GRIDS = 10                       # Total number of grids to generate
TILE_SIZE = (256, 256)               # Resize tiles after kaleidoscoping

def make_kaleidoscope_22_5(img):
    """Create a 22.5° mirrored kaleidoscope tile using one-eighth symmetry."""
    img = img.resize((800, 800))  # Ensure input size is as expected
    center = img.size[0] // 2

    # Rotate, mirror, and composite 8 segments
    result = Image.new("RGBA", img.size)
    for i in range(8):
        angle = i * 45  # 360 / 8 = 45°
        segment = img.rotate(angle, center=(center, center))
        if i % 2 == 1:
            segment = ImageOps.mirror(segment)
        result = Image.alpha_composite(result, segment.convert("RGBA"))

    return result

def load_and_transform_tiles(source_dir):
    files = sorted([os.path.join(source_dir, f) for f in os.listdir(source_dir)
                    if f.lower().endswith('.jpg')])
    
    tiles = []
    for idx, file in enumerate(files, 1):
        print(f"🌀 Generating kaleidoscope tile from source {idx}/{len(files)}: {file}")
        try:
            with Image.open(file) as img:
                img = img.convert("RGBA")
                kaleido = make_kaleidoscope_22_5(img)
                kaleido_resized = kaleido.resize(TILE_SIZE, Image.Resampling.LANCZOS)
                tiles.append(kaleido_resized)
        except Exception as e:
            print(f"⚠️ Skipped {file}: {e}")
    return tiles

def build_grid(tile_images, grid_size):
    tile_w, tile_h = TILE_SIZE
    grid_img = Image.new("RGBA", (tile_w * grid_size, tile_h * grid_size))

    for row in range(grid_size):
        for col in range(grid_size):
            tile = random.choice(tile_images)
            grid_img.paste(tile, (col * tile_w, row * tile_h))

    return grid_img

def main():
    print(f"🔍 Loading and transforming source images from '{SOURCE_DIR}'...")
    tiles = load_and_transform_tiles(SOURCE_DIR)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range(1, NUM_GRIDS + 1):
        print(f"🧩 Building grid {i}/{NUM_GRIDS}...")
        grid = build_grid(tiles, GRID_SIZE)
        output_path = os.path.join(OUTPUT_DIR, f"mandala_grid_8x8_{i}.png")
        grid.save(output_path)
        print(f"✅ Saved: {output_path}")

    print("🎉 Done! All mandala grids generated.")

if __name__ == "__main__":
    main()
