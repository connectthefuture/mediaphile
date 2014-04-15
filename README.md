#Photofile

- Version : 0.1-pre
- Author : Thomas A. Weholt <thomas@weholt.org>
- License : Modified BSD
- WWW : https://github.com/weholt/photofile
- Status : Beta

## About

Photofile is a program (and a collection of reusable methods) for photo/image organization and manipulation.
NB! Photofile is still under active development and there are features that's not fully implemented yet, namely searching
sidecar files and generating thumbnails.

## Warning

When using software that does massive changes to your files, and things like photos and movies in particular, you should
take backups on the files you're going to process before trying to use this program. Photofile comes with no warranties
and may mess your photo-library up completely. So before doing anything test it on a small test-batch of photos and movies
and always backup the files you process, both the master archive and the folders with new content.

## Features

### Relocate photos

Relocates photos and images by EXIF/creation date into a date-based hierarchy.

Example:

    $ photofile -p -s incoming_photos -t processed_photos

### Relocate movies

Relocates movies by creation date into a date-based hierarchy.

Example:

    $ photofile -m -s incoming_movies -t processed_movies

### Find duplicates

Locates duplicates in source folder compared to target folder.

Example:

    $ photofile -d -s different_arhive -t main_archive

Example to delete all duplicates in different_archive folder:

    $ photofile -dx -s different_arhive -t main_archive

### Find new files

Locates new files in source folder compared to target folder.

Example:

    $ photofile -n -s different_arhive -t main_archive


### Generate thumbnails

Creates thumbnails target folder for all photos in source folder.

Example:

    $ photofile -w -s main_archive -t thumbnail_folder

### Search sidecar XMP files for keywords

Example, search for any XMP-file with keywords=beach,sun,summer:

    $ photofile -t main_archive -i keywords=beach,sun,summer


## Installation

To take full advantage of photofile you must install pyexiv2 (http://tilloy.net/dev/pyexiv2/download.html). Since pyexiv2
isn't pip-friendly either download the exe-file if you're on windows or on ubuntu:

    sudo apt-get install python-pyexiv2

Then install photofile using one of these methods:

Alternative a)

    pip install photofile.


Alternative b) download source, unpack and do:

    python setup.py install.


## Command-line/console usage

    $ photofile --help


## Requirements

* pillow or PIL (mandatory)
* pyexiv2 (optional)

## History

Photofile is a refactoring of the reusable django-app called django-photofile. I needed to use some of the code outside django and
refactored out all the utils and metadata methods not directly related to the django-app. Any future releases of
django-photofile will use this package.

- 0.1-pre : first refactoring and initial release of photofile.