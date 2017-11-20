#!/usr/bin/env python
req = ['nose','numpy','pytz','python-dateutil', 'xarray','matplotlib']
# %%
from setuptools import setup,find_packages

setup(name='sciencedates',
      packages=find_packages(),
      version = '1.2.7',
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
      install_requires=req,
      python_requires='>=2.7',
	  )

