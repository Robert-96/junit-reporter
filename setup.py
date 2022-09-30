from setuptools import setup, find_packages

from junit_reporter.__version__ import VERSION


NAME = 'junit-reporter'
KEYWORDS = 'XML, JUnit'
DESCRIPTION = (
    'A Python3 package that generates test results in the standard JUnit XML format for use with Jenkins and other'
    'build integration servers.'
)

URL = 'https://github.com/Robert-96/junit-reporter'
EMAIL = 'dezmereanrobert@gmail.com'
AUTHOR = 'Robert-96'
REQUIRES_PYTHON = '>=3.4.0'
LICENSE = 'GNU GPLv3'

PROJECT_URLS = {
    'Bug Tracker': 'https://github.com/Robert-96/junit-reporter/issues',
    'Documentation': 'https://github.com/Robert-96/junit-reporter/blob/main/README.md',
    'Source': 'https://github.com/Robert-96/junit-reporter'
}

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

with open('README.md') as f:
    README = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    license=LICENSE,
    url=URL,
    project_urls=PROJECT_URLS,

    author=AUTHOR,
    author_email=EMAIL,

    python_requires=REQUIRES_PYTHON,
    setup_requires=REQUIRED,
    install_requires=REQUIRED,
    packages=find_packages(exclude=['tests']),

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Cython',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Operating System :: OS Independent',

        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit',

        'Topic :: Utilities'
    ],
    keywords=KEYWORDS,
)
