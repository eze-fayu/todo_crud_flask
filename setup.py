#!/usr/bin/env python

from distutils.core import setup

setup(
    name='todo_crud_flask',
    version='0.1.0',
    packages=['todo_crud_flask'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],    
    description='A todo-list CRUD app built with Flask + MongoDB',
    author='Andrew Montes',
    author_email='amontes@asyousow.org',    
    long_description=open('README.md').read(),
)