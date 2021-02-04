import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ellipsis",
    version="1.1.20",
    author="Daniel van der Maas",
    author_email="daniel@ellipsis-earth.com",
    description="Package to interact with the Ellipsis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ellipsis-earth/ellipsis-python-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    'pandas',
    'Pillow',
    'geopandas',
    'pyproj',
    'numpy',
    'requests',
    'requests-toolbelt',
    'rasterio',
    'Shapely',
    'geopy',
    'opencv-python',
    'Fiona'
    ],
    python_requires='>=3.6',
)
