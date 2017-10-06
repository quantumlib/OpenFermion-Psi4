import os

from setuptools import setup, find_packages

# This reads the __version__ variable from openfermionpsi4/_version.py
exec(open('openfermionpsi4/_version.py').read())

# Readme file as long_description:
long_description = open('README.rst').read()

# Read in requirements.txt
requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]

setup(
    name='openfermionpsi4',
    version=__version__,
    author='The OpenFermion Developers',
    author_email='help@openfermiong.org',
    url='https://www.openfermion.org/',
    description='A plugin allowing OpenFermion to interface with Psi4.',
    long_description=long_description,
    install_requires=requirements,
    license='GNU Lesser General Public License (LGPL), Version 3 or any later'
            ' version',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': [os.path.join('openfermionpsi4', '_psi4_template')]
    }
)
