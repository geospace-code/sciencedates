#!/usr/bin/env python
req = ['nose','numpy','pytz','python-dateutil','xarray','matplotlib']
# %%
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:    
    pip.main(['install'] + req)
# %%
from setuptools import setup

setup(name='sciencedates',
      packages=['sciencedates'],
      version = '1.2.4',
      description='Date conversions used in the sciences.',
      author = 'Michael Hirsch, Ph.D.',
      url = 'https://github.com/scivision/sciencedates',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: GIS',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      ],
	  )

