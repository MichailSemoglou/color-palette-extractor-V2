# Color Palette Extractor V2.1

This Python script extracts color palettes from images and generates various color harmonies. It's designed for design students and professionals to analyze and utilize color schemes in their projects.

## New in Version 2.1

- **Emotional Color Analysis**: Analyze the psychological impact of colors to guide brand design decisions
- **Enhanced PDF Reports**: Comprehensive reports now include emotional analysis with brand recommendations
- **Improved Error Handling**: More robust handling of edge cases

## Features

- Extract dominant colors from any image
- Generate color harmonies (Complementary, Analogous, Triadic, Tetradic, Tints, and Shades)
- Analyze emotional and psychological effects of colors
- Provide brand design recommendations based on color psychology
- Create a PDF report with visual representation of colors, harmonies, and analysis
- Save color information in a text file for easy reference
- Process single images or entire directories
- Process images recursively in subdirectories
- Parallel processing for improved performance

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/MichailSemoglou/color-palette-extractor-V2.git
   cd color-palette-extractor-V2
   ```

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package and dependencies:

   ```
   pip install -e .
   ```

   Or install just the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. [Download](https://rsms.me/inter/) the Inter font files (Inter-Bold.ttf and Inter-Regular.ttf) and place them in the `color_palette_extractor/fonts` directory.

## Usage

### Command Line Interface

Run the script from the command line as follows:

```
color-palette-extractor-V2 -i path/to/your/image.jpg -o output_folder -n 6
```

#### Options:

- `-i, --image`: Path to a single image file
- `-d, --directory`: Path to a directory of images
- `-f, --file-list`: Path to a text file containing image paths (one per line)
- `-o, --output-dir`: Directory to save results
- `-n, --num-colors`: Number of colors to extract (1-12, default: 6)
- `-j, --jobs`: Number of parallel jobs (default: number of CPU cores)
- `--recursive`: Process directories recursively
- `--no-cache`: Disable caching of results
- `--pdf-only`: Generate only PDF reports (no text files)
- `--text-only`: Generate only text files (no PDF reports)
- `--emotional-analysis`: Include psychological and emotional analysis of colors
- `--log-level`: Set logging level (debug, info, warning, error)
- `--log-file`: Save log to file
- `-v, --version`: Show version information

### Graphical User Interface

To use the GUI, run:

```
python -m color_palette_extractor.gui
```

The GUI allows you to:
- Select individual image files or directories
- Choose output options
- Preview images before processing
- See processing logs in real-time

### Python API

You can also use the library directly in your Python code:

```python
from color_palette_extractor import extract_color_palette, get_harmonies
from color_palette_extractor.output import save_palette_to_pdf, save_palette_and_harmonies
from color_palette_extractor.analysis.emotional import analyze_palette_emotions

# Extract palette from an image
palette = extract_color_palette("path/to/image.jpg", num_colors=6)

# Generate harmonies
harmonies = get_harmonies(palette)

# Generate emotional analysis
emotional_analysis = analyze_palette_emotions(palette)

# Save outputs
save_palette_and_harmonies(palette, harmonies, "output/color_info.txt")
save_palette_to_pdf(
    palette, 
    harmonies, 
    "output/color_palette.pdf", 
    "path/to/image.jpg",
    emotional_analysis=emotional_analysis
)
```

For batch processing:

```python
from color_palette_extractor.batch import process_folder

# Process all images in a directory
result = process_folder(
    "path/to/images",
    num_colors=6,
    output_dir="output",
    recursive=True,
    generate_pdf=True,
    generate_text=True,
    use_cache=True
)

print(f"Processed {result['total']} images")
print(f"Successful: {result['successful']}, Failed: {result['failed']}")
```

## Output Files

The script will generate two output files for each processed image:

1. `{image_name}_info.txt`: A text file containing detailed color information, including:

   - HEX, RGB, and CMYK values for each color in the extracted palette
   - Color harmony information (Complementary, Analogous, Triadic, Tetradic, Tints, and Shades)

2. {image_name}_emotions.txt: A text file containing emotional analysis of the color palette:

   - Overall emotional impact of the palette
   - Harmony analysis and brand recommendations
   - Emotional associations of individual colors

3. `{image_name}_palette.pdf`: A visual report in PDF format, including:
   - The original image
   - The extracted color palette
   - Visual representations of each color harmony
   - Emotional analysis with brand design recommendations

## Emotional Color Analysis

The emotional analysis feature provides insights into the psychological impact of colors:

   - **Dominant Emotions**: The primary emotional responses evoked by the palette
   - **Harmony Analysis**: How the color relationships affect perception
   - **Brand Recommendations**: Suggested industry fits and applications
   - **Individual Color Psychology**: Emotional associations of each color

This feature helps designers make informed decisions about color choices for branding, marketing materials, websites, and other design projects.

## Citation

If you use Color Palette Extractor in your research or design project, please cite it as follows:

`Semoglou, M. (2025). Color Palette Extractor V2.1 [Computer software]. 
Retrieved from https://github.com/MichailSemoglou/color-palette-extractor`

BibTeX:

`@software{semoglou2025colorpalette,
  author = {Semoglou, Michail},
  title = {Color Palette Extractor V2.1},
  year = {2025},
  url = {https://github.com/MichailSemoglou/color-palette-extractor}
}`

## Troubleshooting

Here are some common issues you might encounter and how to resolve them:

1. **ModuleNotFoundError**: If you see an error like `ModuleNotFoundError: No module named 'numpy'`, it means the required dependencies are not installed. Make sure you've run `pip install -r requirements.txt` in your virtual environment.

2. **FileNotFoundError for font files**: If you see an error mentioning `Inter-Bold.ttf` or `Inter-Regular.ttf`, ensure these font files are in the `color_palette_extractor/fonts` directory.

3. **Permission denied when saving output files**: Ensure you have write permissions in the output directory.

4. **Image file not found**: Double-check the path to your image file. Use the full path if the image is not in the same directory as the script.

5. **Out of memory errors**: When processing very large directories, try using smaller batch sizes or reduce the maximum image dimension by editing the configuration.

6. **Process hangs or crashes**: This might occur when processing corrupt or incompatible images. Try using the `--log-level debug` option to identify problematic files.

If you encounter any other issues, please open an issue on the GitHub repository with a detailed description of the problem and the steps to reproduce it.

## Color Harmonies Explanation

1. **Complementary**: Colors opposite each other on the color wheel, creating a high-contrast effect.
2. **Analogous**: Colors adjacent to each other on the color wheel, creating a harmonious and cohesive look.
3. **Triadic**: Three colors evenly spaced on the color wheel, offering a balanced and vibrant color scheme.
4. **Tetradic**: Four colors arranged into two complementary pairs, providing a rich and varied palette.
5. **Tints**: Lighter variations of a color, created by adding white.
6. **Shades**: Darker variations of a color, created by adding black.

## Dependencies

- Python 3.6+
- numpy (1.21.5+)
- scikit-learn (0.24.2+)
- Pillow (8.4.0+)
- reportlab (3.6.2+)
- tqdm (4.64.0+)

For a complete list of dependencies with version information, see `requirements.txt`.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
