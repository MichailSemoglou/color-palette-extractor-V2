from setuptools import setup, find_packages

setup(
    name="color-palette-extractor-V2",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.21.5",
        "scikit-learn>=0.24.2",
        "Pillow>=8.4.0",
        "reportlab>=3.6.2",
        "tqdm>=4.64.0",
    ],
    entry_points={
        "console_scripts": [
            "color-palette-extractor-V2=color_palette_extractor.cli:main",
        ],
    },
    python_requires=">=3.6",
    author="Michail Semoglou",
    description="Extract color palettes from images and generate harmonies",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MichailSemoglou/color-palette-extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "color_palette_extractor": ["fonts/*.ttf"],
    },
)
