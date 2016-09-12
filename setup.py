# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='template',
    version='0.0.1',
    description='Template Layout for Personal Projects.',
    long_description=readme,
    author='Kevin Baugh',
    author_email='me@kkevinbaugh.com',
    url='https://github.com/loraxx753/python_template',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
