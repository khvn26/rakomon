import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'rakomon',
    version = '0.1.2',
    author = 'Kim Gustyr',
    author_email = 'khvn26@gmail.com',
    description = 'Dead simple, configurable monitoring service based on tornado and apscheduler.',
    license = 'MIT',
    keywords = 'simple stupid monitoring',
    url = 'https://github.com/khvn26/rakomon',
    packages=['rakomon'],
    install_requires=[
        'APscheduler',
        'tornado'
    ],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
