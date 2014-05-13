import os
from fabric.api import *

env.hosts = ['localhost']
env.user = 'deploy'
env.directory = os.path.abspath('.')
env.activate = 'source testenv/bin/activate'


def full_test():
    """
    - Creates a new virtual environment
    - installs all required third-party packages
    - installs the mediaphile package
    - runs all unittests
    - removes the virtual environment
    """
    local('virtualenv --no-site-packages venv')
    venv_command = '/bin/bash venv/bin/activate'
    pip_command = 'venv/bin/pip install -r requirements/mandatory.txt'
    local(venv_command + ' && ' + pip_command)
    with lcd(os.path.join(os.curdir, 'tests')):
        local("python testsuite.py")
    local('rm -rf venv')


def base_test():
    """
    - installs the mediaphile package and the exifread package in the current python environment
    - runs all unittests
    """
    local('python setup.py install')
    with lcd(os.path.join(os.curdir, 'tests')):
        local("python testsuite.py")


def test_generation():
    """
    clones https://github.com/ianare/exif-samples into a testfolder and tries to process the contents.
    """
    local('python setup.py install')
    test_area = os.path.join(os.curdir, 'testarea')
    if os.path.exists(test_area):
        local('rm -rf testarea')

    local('mkdir testarea')
    local('mkdir testarea/sorted')
    local('cp -R tests/ testarea/')
    with lcd(test_area):
        local("git clone https://github.com/ianare/exif-samples")
        local('mediaphile -s . -t sorted --verbose')
    #local('rm -rf testarea')
