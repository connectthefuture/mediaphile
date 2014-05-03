from __future__ import with_statement
import os
from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.hosts = ['localhost']
env.user = 'deploy'
env.directory = os.path.abspath('.')
env.activate = 'source testenv/bin/activate'


def full_test():
    local('virtualenv --no-site-packages venv')
    venv_command = '/bin/bash venv/bin/activate'
    pip_command = 'venv/bin/pip install -r requirements/optional.txt'
    local(venv_command + ' && ' + pip_command)
    with lcd(os.path.join(os.curdir, 'tests')):
        local("python testsuite.py")
    local('rm -rf venv')


def base_test():
    local('python setup.py install')
    with lcd(os.path.join(os.curdir, 'tests')):
        local("python testsuite.py")
