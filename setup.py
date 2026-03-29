from setuptools import setup, find_packages

setup(
    name="claws",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "rich>=13.0",
        "pydantic>=2.0",
        "aiohttp>=3.9",
        "jinja2>=3.1",
        "aiohttp-jinja2>=1.6",
    ],
    entry_points={
        "console_scripts": [
            "claws=claws.cli:main",
        ],
    },
)
