#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

with io.open('unityparser/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE
    ).group(1)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='unityparser',
    version=version,
    description='A python library to parse and dump Unity YAML files',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ricard Valverde',
    author_email='ricard.valverde@socialpoint.es',
    url='https://github.com/socialpoint-labs/unity-yaml-parser',
    license='MIT License',
    python_requires='>=3.5.0',
    packages=['unityparser'],
    keywords=['unity','yaml','parser'],
    install_requires=[
        'PyYAML==5.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
