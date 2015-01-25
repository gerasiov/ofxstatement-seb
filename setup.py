#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages
from distutils.core import setup

version = '1.0.0'
with open('README.rst') as f:
    long_description = f.read()

setup(name='ofxstatement-seb',
      version=version,
      author='Alexander Krasnukhin',
      author_email='',
      url='https://github.com/themalkolm/ofxstatement-seb',
      description=('ofxstatement plugins for SEB'),
      long_description=long_description,
      license = 'Apache License 2.0',
      keywords=['ofx', 'ofxstatement', 'seb'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent'
      ],
      packages=find_packages('.'),
      namespace_packages=['ofxstatement', 'ofxstatement.plugins'],
      install_requires=['ofxstatement'],
      test_suite='ofxstatement.plugins.tests',
      include_package_data=True,
      zip_safe=True
)