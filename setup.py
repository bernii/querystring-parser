#!/usr/bin/env python

from distutils.core import setup

setup(
    name="querystring_parser",
    version="1.2.4",
    description="QueryString parser for Python/Django that correctly handles nested dictionaries",
    author="bernii",
    author_email="berni@extensa.pl",
    url="https://github.com/bernii/querystring-parser",
    packages=["querystring_parser"],
    install_requires=["six"],
    classifiers=[
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
