#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import os.path
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from typing import Any

from setuptools import find_packages
from setuptools import setup


def read(*names: Any, **kwargs: dict[str, str]):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fh:  # type: ignore
        return fh.read()


setup(
    name="nsp13",
    version="0.1.0",
    license="MIT",
    description="Interdiciplinary Group Project on finding SARS-CoV-2 NSP13 inhibitors",
    long_description="{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.md")
        ),
    ),
    long_description_content_type="text/markdown",
    author="Anastazja Avdonina, Julia Byrska, Jakub Guzek, Paulina Kucharewicz, Michalina Wysocka",
    url="file://" + os.path.abspath(dirname(__file__)),
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        "Private :: Do Not Upload",
    ],
    keywords=["Machine Learning", "Drug Discovery", "PCM", "nsp13", "SARS-CoV-2"],
    python_requires=">=3.9",
    install_requires=[
        "affine==2.4.0",
        "asttokens==2.2.1",
        "attrs==22.2.0",
        "backcall==0.2.0",
        "biopython==1.80",
        "certifi==2022.12.7",
        "charset-normalizer==3.0.1",
        "click==8.1.3",
        "click-plugins==1.1.1",
        "cligj==0.7.2",
        "coloredlogs==15.0.1",
        "colormath==3.0.0",
        "comm==0.1.3",
        "contourpy==1.0.7",
        "cycler==0.11.0",
        "debugpy==1.6.6",
        "decorator==5.1.1",
        "executing==1.2.0",
        "fonttools==4.38.0",
        "future==0.18.3",
        "graphviz==0.20.1",
        "greenlet==2.0.2",
        "humanfriendly==10.0",
        "idna==3.4",
        "ipykernel==6.22.0",
        "ipython==8.12.0",
        "jedi==0.18.2",
        "Jinja2==3.1.2",
        "jupyter_client==8.1.0",
        "jupyter_core==5.3.0",
        "kiwisolver==1.4.4",
        "lzstring==1.0.4",
        "Markdown==3.4.1",
        "markdown-it-py==2.1.0",
        "MarkupSafe==2.1.2",
        "matplotlib==3.6.3",
        "matplotlib-inline==0.1.6",
        "mdurl==0.1.2",
        "msgpack==1.0.5",
        "multiqc==1.14",
        "neovim==0.3.1",
        "nest-asyncio==1.5.6",
        "networkx==3.0",
        "numpy==1.24.1",
        "packaging==23.0",
        "pandas==1.5.3",
        "parso==0.8.3",
        "pexpect==4.8.0",
        "pickleshare==0.7.5",
        "Pillow==9.4.0",
        "platformdirs==3.2.0",
        "prompt-toolkit==3.0.38",
        "psutil==5.9.4",
        "ptyprocess==0.7.0",
        "pure-eval==0.2.2",
        "Pygments==2.14.0",
        "pynvim==0.4.3",
        "pyparsing==3.0.9",
        "pyproj==3.4.1",
        "python-dateutil==2.8.2",
        "pytz==2022.7.1",
        "PyYAML==6.0",
        "pyzmq==25.0.2",
        "rasterio==1.3.5",
        "requests==2.28.2",
        "rich==13.2.0",
        "rich-click==1.6.1",
        "rioxarray==0.13.3",
        "seaborn==0.12.2",
        "simplejson==3.18.1",
        "six==1.16.0",
        "snuggs==1.4.7",
        "spectra==0.0.11",
        "stack-data==0.6.2",
        "tk==0.1.0",
        "tornado==6.2",
        "traitlets==5.9.0",
        "urllib3==1.26.14",
        "wcwidth==0.2.6",
        "xarray==2023.1.0",
    ],
)
