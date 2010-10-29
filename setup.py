from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(name='pyahooapis',
      version=version,
      description="Yahoo!Japn Text APIs Python wrapper",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='yahoo text jlp',
      author='ukyo',
      author_email='ukyo.web@gmail.com',
      url='http://hujimi.seesaa.net',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
