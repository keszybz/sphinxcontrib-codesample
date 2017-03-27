import sys
import os
import re
if sys.version_info[0] < 3:
    from codecs import open

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as stream:
    long_desc = stream.read()

setup(
    name='sphinxcontrib-codesample',
    version='0.0.0',
    url='https://github.com/keszybz/sphinxcontrib-codesample',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-codesample',
    license='BSD',
    author='Zbigniew Jędrzejewski-Szmek',
    author_email='zbyszek@in.waw.pl',
    description='Sphinx extension to include Python code',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    include_package_data=True,
    install_requires=['Sphinx>=1.1'],
    py_modules = ['sphinxcontrib.codesample_directive'],
)
