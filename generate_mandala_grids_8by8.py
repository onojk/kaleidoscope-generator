import os
import random
from PIL import Image, ImageDraw

# === Settings ===
TILE_DIR = "examples"
OUTPUT_DIR = "generated_grids"
GRID_SIZE = 8
NUM_GRIDS = 10
TILE_SIZE = (256, 256)  # Final size per tile
WEDGE_COUNT = 16  # 360° / 16 = 22.5° per wedge

def load_tiles(tile_dir):
    if not os.path.exists(tile_dir):
        raise FileNotFoundError(f"❌ Tile directory not found: {tile_dir}")

    files = [os.path.join(tile_dir, f) for f in os.listdir(tile_dir)
             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    tiles = []
    for idx, file in enumerate(files, 1):
        print(f"📥 Loading tile {idx}/{len(files)}: {file}")
        try:
            img = Image.open(file).convert("RGBA")
            tiles.append(img)
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    if not tiles:
        raise ValueError("❌ No valid tile images found.")

    return tiles

def random_crop(image, size):
    iw, ih = image.size
    tw, th = size
    if iw < tw or ih < th:
        image = image.resize((max(tw, iw), max(th, ih)), Image.Resampling.LANCZOS)
        iw, ih = image.size
    left = random.randint(0, iw - tw)
    top = random.randint(0, ih - th)
    return image.crop((left, top, left + tw, top + th))

def create_kaleidoscope_tile(image, tile_size, wedge_count=WEDGE_COUNT):
    radius = tile_size[0] // 2
    center = (radius, radius)
    angle = 360 / wedge_count
    base = image.resize((radius * 2, radius * 2), Image.Resampling.LANCZOS)
    base = random_crop(base, (radius * 2, radius * 2))

    tile = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))

    for i in range(wedge_count):
        rotated = base.rotate(-angle * i, center=center)
        mask = Image.new("L", (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([0, 0, radius * 2, radius * 2],
                      i * angle, (i + 1) * angle, fill=255)
        wedge = Image.composite(rotated, Image.new("RGBA", base.size), mask)
        if i % 2 == 1:
            wedge = wedge.transpose(Image.FLIP_LEFT_RIGHT)
        tile = Image.alpha_composite(tile, wedge)

    # Add mirroring & rotated reflections
    h_flip = tile.transpose(Image.FLIP_LEFT_RIGHT)
    v_flip = tile.transpose(Image.FLIP_TOP_BOTTOM)
    rotated_22 = tile.rotate(22.5, center=center)

    # Composite all variants
    final_tile = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    for variant in [tile, h_flip, v_flip, rotated_22]:
        final_tile = Image.alpha_composite(final_tile, variant)

    return final_tile.resize(tile_size, Image.Resampling.LANCZOS)

def build_grid(tile_images, grid_size):
    tile_w, tile_h = TILE_SIZE
    grid_img = Image.new("RGBA", (tile_w * grid_size, tile_h * grid_size))

    for row in range(grid_size):
        for col in range(grid_size):
            base = random.choice(tile_images)
            tile = create_kaleidoscope_tile(base, TILE_SIZE)
            grid_img.paste(tile, (col * tile_w, row * tile_h))

    return grid_img

def main():
    print(f"🔍 Loading tiles from '{TILE_DIR}'...")
    tiles = load_tiles(TILE_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range(1, NUM_GRIDS + 1):
        print(f"\n🌀 Generating Grid {i}/{NUM_GRIDS}...")
        grid = build_grid(tiles, GRID_SIZE)
        output_path = os.path.join(OUTPUT_DIR, f"mandala_grid_8x8_{i}.png")
        grid.save(output_path)
        print(f"✅ Saved: {output_path}")

    print("\n🎉 Done! All mandala grids generated.")

if __name__ == "__main__":
    main()
