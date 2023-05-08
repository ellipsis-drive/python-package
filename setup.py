import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ellipsis",
    version="3.1.11",
    author="Daniel van der Maas",
    author_email="daniel@ellipsis-drive.com",
    description="Package to interact with the Ellipsis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ellipsis-drive-internal/python-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
    'pandas',
    'Pillow',
    'matplotlib',
    'geopandas',
    'pyproj',
    'numpy',
    'imagecodecs',
    'requests',
    'requests-toolbelt',
    'rasterio',
    'Shapely',
    'geopy',
    'scikit-image',
    'Fiona',
    'tifffile'
    ],
    python_requires='>=3.6',
)
