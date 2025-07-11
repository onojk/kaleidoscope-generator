import os
import random
from PIL import Image

# === Settings ===
TILE_DIR = "examples"
OUTPUT_DIR = "generated_grids"
GRID_SIZE = 8
NUM_GRIDS = 10
TILE_SIZE = (256, 256)  # Resize all tiles to this size

def load_tiles(tile_dir):
    if not os.path.exists(tile_dir):
        raise FileNotFoundError(f"❌ Tile directory not found: {tile_dir}")

    files = [os.path.join(tile_dir, f) for f in os.listdir(tile_dir)
             if f.lower().endswith(('.png', '.jpg'))]

    tiles = []
    for idx, file in enumerate(files, 1):
        print(f"📥 Loading tile {idx}/{len(files)}: {file}")
        try:
            img = Image.open(file).convert("RGBA")
            img = img.resize(TILE_SIZE, Image.Resampling.LANCZOS)
            tiles.append(img)
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    if not tiles:
        raise ValueError("❌ No valid tile images found.")

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
    print(f"🔍 Loading tiles from '{TILE_DIR}'...")
    tiles = load_tiles(TILE_DIR)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range(1, NUM_GRIDS + 1):
        grid = build_grid(tiles, GRID_SIZE)
        output_path = os.path.join(OUTPUT_DIR, f"mandala_grid_8x8_{i}.png")
        grid.save(output_path)
        print(f"✅ Saved: {output_path}")

    print("🎉 Done! All mandala grids generated.")

if __name__ == "__main__":
    main()
