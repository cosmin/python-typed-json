import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='typed-json',
      version="0.1",
      description='Python utilities for converting to/from JSON from typed object hierarchies',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/cosmin/python-typed-json',
      download_url='https://github.com/cosmin/python-typed-json',
      author='Cosmin Stejerean',
      author_email='cosmin@offbytwo.com',
      license='Apache License 2.0',
      packages=['typedjson'],
      # test_suite='tests',
      # tests_require=open('test-requirements.txt').readlines(),
      # install_requires=open('requirements.txt').readlines(),
      install_requires=[],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development :: Libraries'
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
      ]
      )
