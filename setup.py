#!/usr/bin/env python
from setuptools import setup, find_packages


setup_requires = [
    'nose',
    'coverage',
]
install_requires = [
    'six',
    'pathlib2>=2.3',
]
tests_require = []


description = "A flexible utility for flattening dict-like objects in Python."

long_description = """\
Please visit  the `GitHub repository <https://github.com/ianlini/flatten-dict>`_
for more information.\n
"""
with open('README.rst') as fp:
    long_description += fp.read()


setup(
    name='flatten-dict',
    version="0.0.3",
    description=description,
    long_description=long_description,
    author='Ian Lin',
    url='https://github.com/ianlini/flatten-dict',
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    license="BSD 2-Clause License",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',
    ],
    test_suite='nose.collector',
    packages=find_packages(),
)
