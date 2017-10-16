================
OpenFermion-Psi4
================

.. image:: https://badge.fury.io/py/openfermionpsi4.svg
    :target: https://badge.fury.io/py/openfermionpsi4

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-brightgreen.svg

`OpenFermion <http://openfermion.org>`__ is an open source library (licensed under Apache 2) for compiling and analyzing quantum algorithms which simulate fermionic systems.
This plugin library allows the electronic structure package `Psi4 <http://psicode.org>`__ (licensed under GNU Lesser General Public License version 3) to interface with OpenFermion.

Installation
------------

To start using OpenFermion-Psi4, first install `Psi4 <http://psicode.org>`__.
Note that Psi4 is designed specifically for the
`Anaconda <https://www.anaconda.com/download>`__ python distribution.
While it is possible to install Psi4 without Anaconda, if one does use Anaconda python
the following commands will install Psi4 and pip (used to install OpenFermion-Psi4):

.. code-block:: bash

  conda config --add channels http://conda.anaconda.org/psi4
  python -m conda install psi4
  python -m conda install pip

To install the latest versions of OpenFermion and OpenFermion-Psi4 (in development mode):

.. code-block:: bash

  git clone https://github.com/quantumlib/OpenFermion-Psi4
  cd OpenFermion-Psi4
  python -m pip install -e .

Alternatively, to install the latest PyPI releases as libraries (in user mode):

.. code-block:: bash

  python -m pip install --pre --user openfermionpsi4

Also be sure to take a look at the `ipython notebook demo <https://github.com/quantumlib/OpenFermion-Psi4/blob/master/examples/openfermionpsi4_demo.ipynb>`__.

How to contribute
-----------------

We'd love to accept your contributions and patches to OpenFermion-Psi4.
There are a few guidelines you need to follow.
Contributions to OpenFermion-Psi4 must be accompanied by a Contributor License Agreement.
You (or your employer) retain the copyright to your contribution,
this simply gives us permission to use and redistribute your contributions as part of the project.
Head over to https://cla.developers.google.com/
to see your current agreements on file or to sign a new one.

All submissions, including submissions by project members, require review.
We use GitHub pull requests for this purpose. Consult
`GitHub Help <https://help.github.com/articles/about-pull-requests/>`__ for
more information on using pull requests.
Furthermore, please make sure your new code comes with extensive tests!
We use automatic testing to make sure all pull requests pass tests and do not
decrease overall test coverage by too much. Make sure you adhere to our style
guide. Just have a look at our code for clues. We mostly follow
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ and use
the corresponding `linter <https://pypi.python.org/pypi/pep8>`_ to check for it.
Code should always come with documentation.

Authors
-------

`Ryan Babbush <http://ryanbabbush.com>`__ (Google),
`Jarrod McClean <http://jarrodmcclean.com>`__ (Google),
`Ian Kivlichan <http://aspuru.chem.harvard.edu/ian-kivlichan/>`__ (Harvard),
`Damian Steiger <https://github.com/damiansteiger>`__ (ETH Zurich),
`Thomas Haener <https://github.com/thomashaener>`__ (ETH Zurich) and
`Dave Bacon <https://github.com/dabacon>`__ (Google).

Disclaimer
----------
Copyright 2017 The OpenFermion Developers.
This is not an official Google product.
