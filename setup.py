# setup.py
from setuptools import setup, find_packages

setup(
    name="pqc_compare",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
    ],
    # Add path to liboqs shared library
    package_data={
        "pqc_compare": ["../liboqs/build/lib/*"],
    }
)