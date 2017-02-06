import os
import sys

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# reading requirements
install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]
sys.path.insert(0, os.path.dirname(__file__))
setup(
    name='agua',
    version='0.1',
    packages=find_packages(),
    install_requires=reqs,
    description='Compare data in columns with other columns with the help of comparator functions',
    long_description='Compare data in columns with other columns with the help of comparator functions',
    keywords = ['agua', 'testing', 'data', 'csv'],
    url='https://github.com/CompileInc/agua',
    download_url = 'https://github.com/CompileInc/agua/archive/v{version}.tar.gz'.format(version=version),
    entry_points='''
        [console_scripts]
        agua=agua:cli
    '''
)
