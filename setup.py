from setuptools import setup

setup(
    name="dd",
    version="0.0.1",
    description="Some dbt debugging tools.",
    packages=["src"],
    url="https://gitlab.com/jeremyyeo/dd",
    entry_points={"console_scripts": ["dd = src.__main__:main"]},
)
