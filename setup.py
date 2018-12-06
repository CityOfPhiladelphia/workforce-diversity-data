#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Workforce Diversity',
    version='1.0',
    packages=['workforce_diversity',],
    description='Transforms workforce diversity data',
    long_description=open('README.md').read(),
    install_requires=[
      'arrow==0.12.0',
      'click==6.7',
      'petl==1.1.1',
      'xlrd==1.0.0',
      'xlwt-future==0.8.0',
    ],
    entry_points={
        'console_scripts': [
            'workforce_diversity=workforce_diversity:main',
        ],
    }
)
