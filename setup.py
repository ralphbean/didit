from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='didit',
      version=version,
      description="Commandline tool to remember what I did last week",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/didit',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      scripts=[
          "scripts/didit-remember",
          "scripts/didit-report"
      ],
      install_requires=[
          "tw2.core",
          "mako",
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
