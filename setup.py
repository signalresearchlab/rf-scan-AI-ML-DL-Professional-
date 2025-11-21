#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rf-scanner-ai",
    version="1.0.0",
    author="Signal Research Lab",
    author_email="signalresearchlab@gmail.com",
    description="Advanced RF Signal Detection & Analysis with AI/ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/signalresearchlab/rf-scan-AI-ML-DL-Professional",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Communications :: Ham Radio",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "flask>=2.0.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.5.0",
        "scikit-learn>=1.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rf-scan=cli:cli",
        ],
    },
    include_package_data=True,
)
