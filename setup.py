"""Install fchic."""
import setuptools

setuptools.setup(
    name="fchic",
    version="0.1.0",
    author="Cyrille Lavigne",
    author_email="cyrille.lavigne@mail.utoronto.ca",
    description="",
    url="https://github.com/aspuru-guzik-group/fchic",
    package_dir={"": "src"},
    package_data={"fchic": ["py.typed"]},  # mypy exports
    packages=setuptools.find_namespace_packages(where="src"),
    # Dependencies
    python_requires=">=3.7",
    install_requires=[
        "pyparsing",
    ],
)
