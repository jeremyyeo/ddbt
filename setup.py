from setuptools import setup

setup(
    name="ddbt",
    version="0.0.1",
    description="Some dbt debugging tools.",
    packages=["src"],
    url="https://gitlab.com/jeremyyeo/ddbt",
    entry_points={"console_scripts": ["ddbt = src.__main__:main"]},
)
