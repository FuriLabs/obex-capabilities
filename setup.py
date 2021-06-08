#!/usr/bin/env python3

import re
import ast
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from codecs import open
from os import path


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


here = path.abspath(path.dirname(__file__))
_version_re = re.compile(r'VERSION\s+=\s+(.*)')

with open(path.join(here, 'obex_capabilities/__init__.py'), 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='obex-capabilities',
    version=version,
    description='Simple script to generate OBEX capabilities XML files'
                'at runtime for Bluetooth OBEX support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='postmarketOS Developers',
    author_email='info@postmarketos.org',
    url='https://www.postmarketos.org',
    license='GPLv3',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='obex capabilities bluetooth',
    data_files=[('data', ['data/template.xml'])],
    packages=find_packages(exclude=['data', 'tests']),
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'obex-capabilities=obex_capabilities:main',
        ],
    },
    include_package_data=True,
)

