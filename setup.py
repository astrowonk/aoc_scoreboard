import setuptools
from aoc_scoreboard import __VERSION__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aoc_scoreboard",
    version=__VERSION__,
    author="Marcos Huerta",
    author_email="marcos@marcoshuerta.com",
    description=
    "Load local scoreboard data from Advent of Code to pandas dataframes",
    install_requires=["pandas"],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astrowonk/aoc_scoreboard",
    #packages=setuptools.find_packages(),
    py_modules=['aoc_scoreboard'],
    #   entry_points={"console_scripts": ["gpxcsv=gpxcsv.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)