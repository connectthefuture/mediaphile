#/usr/bin/env python

import os
from setuptools import setup, find_packages


setup(
    name = "MediaPhile",
    version = "0.1-pre",
    author = "Thomas Weholt",
    author_email = "thomas@weholt.org",
    description = ("A collection of programs and a library of reusable methods for organization and manipulation of photos and movies."),
    license = "Modified BSD",
    keywords = "photo movie thumbnail organization generation metadata",
    url = "https://github.com/weholt/mediaphile",
    install_requires = ['pillow', 'exifread',],
    zip_safe = False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        ],
    packages = find_packages(),
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    entry_points = {
        'console_scripts': [
            'mediaphile = mediaphile.cli.photo:main',
            'mediaphile.xmp = mediaphile.cli.xmp:main',
            'mediaphile.db = mediaphile.cli.db:main',
            'mediaphile.file = mediaphile.cli.file:main',
            'mediaphile.gps = mediaphile.cli.gps:main',
            'mediaphile.movies = mediaphile.cli.movies:main',
            'mediaphile.thumbnails = mediaphile.cli.thumbnails:main',
            'mediaphile.inotify = mediaphile.cli.inotify:main',
            ],
        },
)