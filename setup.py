from setuptools import setup, find_packages

__version__ = "0.1"

setup(
    name="bubble",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-restful",
        "flask-jwt-extended",
        "flask-marshmallow",
        "python-dotenv",
        "pymongo",
        "mongoengine",
        "environs",
        "passlib",
        "apispec[yaml]",
        "apispec-webframeworks",
    ],
    entry_points={
        "console_scripts": [
            "bubble = bubble.manage:cli"
        ]
    },
)
