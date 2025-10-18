#!/usr/bin/env python3
"""
Setup script for FactScreen API
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="factscreen-api",
    version="0.1.0",
    author="FactScreen Team",
    author_email="team@factscreen.com",
    description="A comprehensive fact-checking API that combines multiple sources and uses AI for claim analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/factscreen/factscreen-api",
    packages=find_packages(where="factscreen_backend"),
    package_dir={"": "factscreen_backend"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-asyncio",
            "httpx",
        ],
    },
    entry_points={
        "console_scripts": [
            "factscreen-server=app.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
