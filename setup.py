from setuptools import setup
from os import path

current_directory = path.dirname(path.abspath(__file__))

with open(path.join(current_directory, "README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name="nima",
    version="1.0.0",
    author="Taavi Väänänen",
    author_email="hi@taavi.wtf",
    description="Utility for managing development nginx config files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supertassu/nima",
    install_requires=[
        line.strip()
        for line in open(path.join(current_directory, "requirements.txt"), "r")
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: System Administrators",
    ],
    python_requires=">=3.6",
    packages=["nima"],
    entry_points="""
    [console_scripts]
    nima=nima.cli:cli
""",
)
