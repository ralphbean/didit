from setuptools import setup, find_packages
import sys, os

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

version = '0.1.5'

setup(name='didit',
      version=version,
      description="Lightweight, commandline tool to remember what I did last week",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Natural Language :: English",
          "Topic :: Office/Business :: News/Diary",
          "Topic :: Text Processing :: Markup",
          "Topic :: Utilities",
      ],
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
