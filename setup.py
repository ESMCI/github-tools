import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="esmci-github-tools",
    version="0.1",
    author="Bill Sacks",
    author_email="sacks@ucar.edu",
    description="Tools for working with GitHub repositories from the command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ESMCI/github-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "PyGithub",
    ],
    scripts=[
        "gh-pr-query",
    ],
)
