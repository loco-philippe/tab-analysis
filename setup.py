# -*- coding: utf-8 -*-
"""
`tab_analysis` setup
"""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tab_analysis",
    version="0.2.0",
    description="TAB-analysis : A tool to analyse tabular and multi-dimensionnal structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loco-philippe/tab-analysis/blob/main/README.md",
    author="Philippe Thomy",
    author_email="philippe@loco-labs.io",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="tabular data, multidimensional data, open data, environmental data",
    packages=find_packages(include=["tab_analysis", "tab_analysis.*"]),
    python_requires=">=3.9, <4",
    install_requires=[],
)
