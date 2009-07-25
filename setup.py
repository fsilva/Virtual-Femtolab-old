#!/usr/bin/env python

from distutils.core import setup

setup(name='Virtual FemtoLab',
      version='alpha 1',
      description='Virtual Ultrafast Optics Laboratory',
      author='Francisco Silva',
      author_email='fsilvaportugal@gmail.com',
      url='MISSING_URL',
      packages=['VirtualFemtolab'],
      package_data={'VirtualFemtolab':['data/*']},
      scripts=['virtualfemtolab'],
      data_files=[('data','*')]
     )


