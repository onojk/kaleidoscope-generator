Kaleidoscope Generator 🌀

This project generates mandala-style kaleidoscope tile grids using source images. Each tile is a mirrored 22.5° radial kaleidoscope, assembled into 8x8 grids. Every grid uses a single source image with randomized sampling for visual diversity.

✨ Features

- Converts input images into 22.5° mirrored kaleidoscope tiles
- Builds high-resolution 8x8 mandala-style grids
- Each grid is themed on one source image
- Fully randomized tile samples within each theme
- Batch generation for multiple grids
- Clean RGBA output with transparency preserved

📂 Project Structure

.
├── examples/                     # Input source images (JPG or PNG)
├── generated_grids/             # Output kaleidoscope tiles and grid PNGs
├── generate_mandala_grids_8by8.py  # Main script
└── README.md

🖼️ Example Output

Grid 1 - generated_grids/mandala_grid_8x8_1.png
Grid 2 - generated_grids/mandala_grid_8x8_2.png
Grid 3 - generated_grids/mandala_grid_8x8_3.png

▶️ How to Use

1. Add Source Images
Place .jpg or .png files in the examples/ directory. Each image will be used as the "theme" for one 8x8 kaleidoscope grid.

2. Run the Generator
Make sure you're in your Python virtual environment if using one.

    python3 generate_mandala_grids_8by8.py

This will generate multiple files inside generated_grids/:
- kaleidoscope_theme_N.png: A visual reference for the theme image used in each grid.
- mandala_grid_8x8_N.png: The final tiled kaleidoscope grid.

⚙️ Requirements

- Python 3.7 or higher
- Pillow (Python Imaging Library fork)

Install with pip:

    pip install pillow

💡 Project Motivation

This tool celebrates the meditative, symmetrical beauty of kaleidoscopic art. It’s built to transform everyday images into vibrant mandala-style patterns, perfect for creative exploration or digital wallpaper design.

📜 License

MIT License

🙏 Acknowledgments

Created by https://github.com/onojk — open source and community-supported.
