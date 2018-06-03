from codecs import open
from os import path
from setuptools import setup, find_packages

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mongo-user-blueprint",
    version="0.1.0",
    description="MongoDB user handling demo based on the user-blueprint project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/volfpeter/user-blueprint",
    author="Peter Volf",
    author_email="do.volfp@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="flask blueprint user mongodb authentication login registration session templates argon2",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.5",
    install_requires=[
        "pymongo>=3.6",
        "user-blueprint>=0.3"
    ]
)
