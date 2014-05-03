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
    pip_command = 'venv/bin/pip install -r requirements/optional.txt'
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
