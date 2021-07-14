"""Install fchic."""
import setuptools
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="fchic",
    version="0.1.1",
    author="Cyrille Lavigne",
    author_email="cyrille.lavigne@mail.utoronto.ca",
    description="fchic is a minimal parser for Gaussian 16 formatted checkpoint files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clavigne/fchic",
    package_dir={"": "src"},
    package_data={"fchic": ["py.typed"]},  # mypy exports
    packages=setuptools.find_namespace_packages(where="src"),
    license="MIT",
    # Dependencies
    python_requires=">=3.7",
    install_requires=[
        "pyparsing",
        'importlib-metadata ~= 1.0 ; python_version < "3.8"',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        #
        "Typing :: Typed",
        #
        "License :: OSI Approved :: MIT License",
        #
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        #
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="chemistry gaussian16 g16",
)
