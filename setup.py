# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='vinci',
    version='0.0.1',
    description='A low level terminal app framework using curses, pyfiglet, and a few other things..',
    long_description=readme,
    author='Kevin Baugh',
    author_email='me@kkevinbaugh.com',
    url='https://github.com/loraxx753/Vinci',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
