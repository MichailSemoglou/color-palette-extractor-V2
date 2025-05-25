# Color Palette Extractor V2.1

A Python tool that extracts color palettes from images, generates various color harmonies, and provides psychological and emotional analysis of colors for brand design.

## Features

- Extract dominant colors from any image using K-means clustering
- Generate color harmonies (Complementary, Analogous, Triadic, Tetradic, Tints, and Shades)
- Analyze emotional and psychological effects of colors with brand design recommendations
- Create comprehensive PDF reports with visual representation of colors and harmonies
- Save color information in structured text files for easy reference
- Process single images, multiple files, or entire directories in parallel
- Cache results to avoid reprocessing previously analyzed images
- Use via command-line or graphical user interface

## What's New in Version 2.1

- **Emotional Color Analysis**: Psychological impact assessment of colors for brand design
- **Enhanced PDF Reports**: Comprehensive reports with emotional analysis and brand recommendations
- **Improved Error Handling**: More robust handling of edge cases and error conditions
- **Better Documentation**: Expanded documentation and code comments

## Installation

### Prerequisites

- Python 3.8 or higher
- Required packages: numpy, scikit-learn, Pillow, reportlab, tqdm

### Quick Install

```bash
# Clone the repository
git clone https://github.com/MichailSemoglou/color-palette-extractor-V2.git
cd color-palette-extractor-V2

# Set up a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install the package and dependencies
pip install -e .
```

### Font Installation

This tool uses the Inter font for its PDF reports. You'll need to:

1. [Download Inter fonts](https://rsms.me/inter/) (specifically Inter-Bold.ttf and Inter-Regular.ttf)
2. Create a `fonts` directory under `color_palette_extractor` if it doesn't exist
3. Place the downloaded font files in the `color_palette_extractor/fonts` directory

If the Inter fonts are not available, the tool will automatically fall back to standard fonts.

## Usage

### Command Line Interface

```bash
# Process a single image with default settings
color-palette-extractor-V2 -i path/to/image.jpg

# Process with specific options
color-palette-extractor-V2 -i path/to/image.jpg -o output_folder -n 8 --emotional-analysis

# Process all images in a directory
color-palette-extractor-V2 -d path/to/images/ -o output_folder --recursive

# Process images listed in a file
color-palette-extractor-V2 -f image_list.txt -o output_folder
```

#### Command-Line Options

| Option | Description |
| ------ | ----------- |
| `-i, --image PATH` | Path to a single image file |
| `-d, --directory PATH` | Path to a directory of images |
| `-f, --file-list PATH` | Path to a text file containing image paths (one per line) |
| `-o, --output-dir PATH` | Directory to save results (default: same as input) |
| `-n, --num-colors N` | Number of colors to extract (1-12, default: 6) |
| `-j, --jobs N` | Number of parallel jobs (default: number of CPU cores) |
| `--recursive` | Process directories recursively |
| `--no-cache` | Disable caching of results |
| `--pdf-only` | Generate only PDF reports (no text files) |
| `--text-only` | Generate only text files (no PDF reports) |
| `--emotional-analysis` | Include psychological and emotional analysis of colors |
| `--log-level LEVEL` | Set logging level (debug, info, warning, error) |
| `--log-file PATH` | Save log to specified file |
| `-v, --version` | Show version information |

### Graphical User Interface

For a more user-friendly experience, you can use the graphical interface:

```bash
python -m color_palette_extractor.gui
```

The GUI allows you to:
- Select individual image files or entire directories
- Configure output options and settings
- Preview images before processing
- Monitor processing logs in real-time

### Python API

You can also use the tool as a library in your Python code:

```python
from color_palette_extractor import extract_color_palette, get_harmonies
from color_palette_extractor.output import save_palette_to_pdf, save_palette_and_harmonies
from color_palette_extractor.analysis.emotional import analyze_palette_emotions

# Extract colors from an image
palette = extract_color_palette("path/to/image.jpg", num_colors=6)

# Generate color harmonies
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
    use_cache=True,
    config={"emotional_analysis": True}
)

print(f"Processed {result['total']} images")
print(f"Successful: {result['successful']}, Failed: {result['failed']}")
```

## Output Files

For each processed image, the tool generates:

### 1. Color Information Text File

`{image_name}_info.txt` contains:
- HEX, RGB, and CMYK values for each color in the extracted palette
- Color harmony information (Complementary, Analogous, Triadic, Tetradic, Tints, Shades)

### 2. Emotional Analysis Text File

`{image_name}_emotions.txt` provides:
- Overall emotional impact of the palette
- Harmony analysis and brand suitability
- Individual emotional associations for each color

### 3. Visual PDF Report

`{image_name}_palette.pdf` includes:
- The original image
- Visual representation of the extracted color palette
- Color harmony visualizations
- Emotional analysis with brand design recommendations

## Understanding Color Harmonies

The tool generates several types of color harmonies:

| Harmony Type | Description |
| ------------ | ----------- |
| **Complementary** | Colors opposite each other on the color wheel, creating high contrast |
| **Analogous** | Colors adjacent to each other on the color wheel, creating cohesion |
| **Triadic** | Three colors evenly spaced on the color wheel, providing balance |
| **Tetradic** | Four colors arranged in two complementary pairs, offering variety |
| **Tints** | Lighter variations of a color (adding white) |
| **Shades** | Darker variations of a color (adding black) |

### Color Accuracy Note

The emotional analysis feature maps extracted colors to a predefined set of color categories in our database. Since we work with a finite number of color definitions, some matches may not be entirely accurate, particularly for:

- Colors that fall between our predefined categories (e.g., a blue-green might be categorized as either blue or green)
- Very specific shades that don't have exact matches in our color database
- Unique or unusual colors that may be mapped to their nearest neighbor
- Colors with subtle variations that might all map to the same category

The tool provides its best interpretation by finding the closest match in our color database. For critical color analysis applications, consider:
- Treating the emotional analysis as a general guide rather than absolute categorization
- Manually verifying color interpretations for important branding decisions

## Emotional Color Analysis

The emotional analysis feature provides insights into:

- **Dominant Emotions**: Primary emotional responses evoked by the palette
- **Harmony Analysis**: How color relationships affect perception
- **Brand Recommendations**: Suggested industry fits and applications
- **Individual Color Psychology**: Emotional associations for each color

This helps designers make informed decisions about color choices for branding, marketing materials, websites, and other design projects.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure you've installed all dependencies with `pip install -r requirements.txt`

2. **Font related errors**: If you see errors mentioning Inter fonts, follow the font installation steps above

3. **Permission denied when saving output**: Check that you have write permissions in the output directory

4. **Memory errors with large directories**: Try reducing the maximum image dimension in the configuration or process fewer images at once

5. **Process hangs or crashes**: Use the `--log-level debug` option to identify problematic files

### Advanced Configuration

For advanced users, configuration can be customized:

1. Create a configuration file at `~/.color_extractor_config.json`
2. Add configuration options like:

```json
{
  "num_colors": 8,
  "max_dimension": 1000,
  "cache_dir": ".cache",
  "pdf_options": {
    "page_size": "A4",
    "margin": 36,
    "show_original_image": true
  }
}
```

## Development

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/MichailSemoglou/color-palette-extractor-V2.git
cd color-palette-extractor-V2

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Citation

If you use this tool in your research or design project, please cite it as:

```
Semoglou, M. (2025). Color Palette Extractor V2.1 [Computer software]. 
Retrieved from https://github.com/MichailSemoglou/color-palette-extractor-V2
```

BibTeX:
```bibtex
@software{semoglou2025colorpalette,
  author = {Semoglou, Michail},
  title = {Color Palette Extractor V2.1},
  year = {2025},
  url = {https://github.com/MichailSemoglou/color-palette-extractor-V2}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
