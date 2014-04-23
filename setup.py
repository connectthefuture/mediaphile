#/usr/bin/env python

import os
from setuptools import setup, find_packages


setup(
    name = "Photofile",
    version = "0.1-pre",
    author = "Thomas Weholt",
    author_email = "thomas@weholt.org",
    description = ("A collection of utils for organization and manipulation of photos and movies."),
    license = "Modified BSD",
    keywords = "photo movie thumbnail organization generation metadata",
    url = "https://github.com/weholt/photofile",
    install_requires = ['pillow',],
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
            'photofile = photofile.cli:main',
            'photofile.xmp = photofile.cli.xmp:main',
            'photofile.db = photofile.cli.db:main',
            'photofile.file = photofile.cli.file:main',
            'photofile.gps = photofile.cli.gps:main',
            'photofile.movies = photofile.cli.movies:main',
            'photofile.thumbnails = photofile.cli.thumbnails:main',
            'photofile.inotify = photofile.cli.inotify:main',
            ],
        },
)