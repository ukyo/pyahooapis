from setuptools import setup, find_packages
import sys, os

version = '0.2.2'

setup(name='pyahooapis',
      version=version,
      description="Yahoo! Japan Text APIs Python wrapper",
      long_description="""\
Setup
-----
::

  $ easy_install pyahooapis

Example
-------
.. sourcecode::

  from pyahooapis import jlp
  
  appid = 'your-application-id'
  api = jlp.JLPAPIs(appid)
  sentence = 'sentence'
  
  chunks = api.da.get_chunks(sentence)
  
  for chunk in chunks:
      print '%s -> %s' % (chunk, chunks[chunk.dependency] if chunk.dependency != -1 else None)
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='yahoo text jlp',
      author='ukyo',
      author_email='ukyo.web@gmail.com',
      url='https://github.com/ukyo/pyahooapis',
      license='Apache License 2.0',
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
