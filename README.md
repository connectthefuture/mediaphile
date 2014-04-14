#Photofile

- Version : 0.1-pre
- Author : Thomas A. Weholt <thomas@weholt.org>
- License : Modified BSD
- WWW : https://github.com/weholt/photofile
- Status : Beta

## About

Photofile is a program (and a collection of reusable methods) for photo/image organization and manipulation. It's is a
refactoring of the reusable django-app called django-photofile. I needed to use some of the code outside django and
refactored out all the utils and metadata methods not directly related to the django-app. Any future releases of
django-photofile will use this package.

## Installation

To take full advantage of photofile you must install pyexiv2 (http://tilloy.net/dev/pyexiv2/download.html). Since pyexiv2
isn't pip-friendly either download the exe-file if you're on windows or on ubuntu:

        using sudo apt-get install python-pyexiv2

Then install photofile using one of these methods:

* Alternative a:

        pip install photofile.


* Alternative b) download source, unpack and do:

        python setup.py install.


## Usage

        $ photofile --help


## Requirements

* pillow or PIL (mandatory)
* pyexiv2 (optional)
