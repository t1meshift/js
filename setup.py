from setuptools import setup
from jasminesnake import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="jasminesnake",
    version=__version__,
    packages=["jasminesnake"],
    url="https://github.com/t1meshift/js",
    license="MIT",
    author="Yury Kurlykov",
    author_email="sh1ftr@protonmail.ch",
    description="Another JavaScript interpreter written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        # "Programming Language :: JavaScript",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={"console_scripts": ["jasminesnake = jasminesnake.__main__:main"]},
)
