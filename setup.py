# setup.py
from setuptools import setup, find_packages

setup(
    name="markdown-equations-fixer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "meq-fixer=markdown_equations_fixer.cli:cli",
        ],
    },
    author="Vivek Singh",
    author_email="vs15vivek@gmail.com",
    description="A CLI tool to fix mathematical equations in markdown files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vs15vivek/markdown-equations-fixer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
