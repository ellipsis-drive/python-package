import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ellipsis",
    version="1.1.7",
    author="Daniel van der Maas",
    author_email="daniel@ellipsis-earth.com",
    description="Package to interact with the Ellipsis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ellipsis-earth/ellipsis-python-package",
    packages=['pandas', 'Pillow', 'geopandas', 'pyproj', 'numpy', 'requests', 'rasterio', 'shapely', 'geopy','cv2', 'owslib', 'requests_toolbelt' ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
