#MediaPhile

- Version : 0.1-pre
- Author : Thomas A. Weholt <thomas@weholt.org>
- License : Modified BSD
- WWW : https://github.com/weholt/mediaphile
- Status : Alpha, incomplete.

## About

MediaPhile is a collection of program/scripts (and a library of reusable methods) for photo/image organization and
manipulation. MediaPhile is first and foremost a solution aimed at photographers, with focus on processing metadata like
EXIF and IPTC.

When MediaPhile has been installed some programs will be placed in your python/bin or python/scripts folder:

### mediaphile

The main program. Generates date-based folder hierarchy based on information found in EXIF-data in the photos.

To get help and see what options are available:

    mediaphile --help

Example:

    $ mediaphile -s incoming_photos -t processed_photos

### mediaphile.movies

Organizes movies into a date-based folder hierarchy based on the creation date of the movie.

Example:

    $ mediaphile.movies -s incoming_movies -t processed_movies

### mediaphile.xmp

Search XMP metadata and list matching photos.

Example, search for any XMP-file with keywords=beach,sun,summer:

    $ mediaphile.xmp -t main_archive -i keywords=beach,sun,summer

NOT IMPLEMENTED AT ALL.

### mediaphile.thumbnails

Generates thumbnails.

Example:

    $ mediaphile.thumbnails -s main_archive -t thumbnail_folder -o 400x400 --crop

You can also create thumbnails in several resolutions at once:

    $ mediaphile.thumbnails -s main_archive -t thumbnail_folder -o 400x400,800x600,1024x768

If any information about orientation is found in the EXIF metadata the photos will automatically be rotated.

NOT IMPLEMENTED FULLY YET.

### mediaphile.gps

Process photos based on GPS information found in EXIF-data in the photos.

NOT IMPLEMENTED AT ALL.

### mediaphile.file

General methods for finding new or duplicate content in two folders.

Show all duplicate files in one folder compared to another folder:

    $ mediaphile.file -s different_arhive -t main_archive

Example to delete all duplicates in different_archive folder:

    $ mediaphile.file -d -s different_arhive -t main_archive

Show all new files in one folder compared to another folder:

    $ mediaphile.file -n -s different_arhive -t main_archive

### mediaphile.db

Handles generation of a metadata database for faster searches.

NOT IMPLEMENTED AT ALL.

### mediaphile.inotify

Program that monitors a specific folder and reacts when files are added.

NOT IMPLEMENTED AT ALL.

## Warning

NB! MediaPhile is still under active development and there are several features that's not fully implemented yet.

When using software that does massive changes to your files, and things like photos and movies in particular, you should
take backups of the files you're going to process before trying to use this program. MediaPhile comes with no warranties
and may mess your photo-library up completely. So before doing anything test it on a small test-batch of photos and movies
and always backup the files you process, both the master archive and the folders with new content.

## Installation

Then install mediaphile using one of these methods:

Alternative a)

    pip install mediaphile

Alternative b) download source, unpack and do:

    python setup.py install

The line above will install mediaphile and the only mandatory third-party libraries Pillow and exifread. To enable all available features you must
install the optional third-party libraries:

If you downloaded the complete source code:

    pip install -r requirements/optional.txt

Or if you did just pip install mediaphile:

    pip install -r https://raw.githubusercontent.com/weholt/mediaphile/master/requirements/optional.txt

## Requirements

* pillow or PIL (mandatory)
* exifread (mandatory)
* BeautifulSoup ( http://www.crummy.com/software/BeautifulSoup/, optional - for parsing XMP-files)
* lxml (http://lxml.de/, optional but required by BeautifulSoup)
* pyinotify (https://github.com/seb-m/pyinotify, optional - for watching a folder for photos)

## History

MediaPhile is a refactoring of the reusable django-app called django-photofile. I needed to use some of the code outside django and
refactored out all the utils and metadata methods not directly related to the django-app. Any future releases of
django-photofile will use this package.

- 0.1-pre : first refactoring and initial release of mediaphile.