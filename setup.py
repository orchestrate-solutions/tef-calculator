"""Setup configuration for tef-calculator."""
from setuptools import setup, find_packages

setup(
    name="tef-calculator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
