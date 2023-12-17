from setuptools import setup, find_packages
import os
import re

# Function to read the README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Function to parse version from __init__.py
def get_version():
    with open(os.path.join('AsyncPyToolbox', '__init__.py'), 'r', encoding='utf-8') as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Version not found.")

setup(
    name='AsyncPyToolBox',
    version=get_version(),
    description='A collection of useful functions and classes for Python.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='WarnerStark',
    author_email='starktechfriday@gmail.com',
    url='https://github.com/TelegramExtended/AsyncPyToolBox',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=["asyncpytoolbox", "asyncpy", "asyncpytool"],
    include_package_data=True,
)
