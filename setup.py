#!/usr/bin/env python
import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = [
    'pytest',
    'sanic',
    'aiohttp',
]

tests_require = []

setup(name='pytest-sanic',
      version='0.1.6',
      description='',
      long_description=open(README_PATH).read(),
      author='Yun Xu',
      author_email='yunxu1992@gmail.com',
      url='',
      packages=find_packages(),
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ],
      entry_points={
        'pytest11': ['sanic = pytest_sanic.plugin'],
      },
)
