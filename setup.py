#!/usr/bin/env python

from os import path
from setuptools import setup, find_packages

BASE_DIR = path.abspath(path.dirname(__file__))


def read(f):
    with open(path.join(BASE_DIR, f)) as fh:
        return fh.read()


def get_version():
    version = read('VERSION').strip()
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


install_requires = []

setup(
    name='secure',
    version=get_version(),
    description='Provides standard interface for hashing, encrypting, decrypting and verifying user input',
    long_description=read('README.md'),
    author='Integralist',
    url='https://github.com/integralist/Python-Encryption',
    packages=find_packages(),
    install_requires=install_requires,
    keywords='integralist hash hashing encryption decryption library scrypt'
)
