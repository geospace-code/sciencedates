#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = ['numpy', 'pytz', 'python-dateutil']
tests_require = ['pytest', 'nose', 'coveralls', 'flake8', 'mypy']
# %%

setup(name='sciencedates',
      packages=find_packages(),
      version='1.4.1',
      description='Date conversions used in the sciences.',
      long_description=open('README.rst').read(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/sciencedates',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: GIS',
      ],
      install_requires=install_requires,
      python_requires='>=3.6',
      tests_require=tests_require,
      extras_require={'tests': tests_require,
                      'plot': ['xarray', 'matplotlib']},
      scripts=['date2doy.py', 'randomdate.py'],
      )
