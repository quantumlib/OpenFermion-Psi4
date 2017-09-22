OpenFermion-Psi4
================

`OpenFermion <http://openfermion.org>`__ is an open source library (licensed under Apache 2) for compiling and analyzing quantum algorithms which simulate fermionic systems.
This plugin library allows the electronic structure package `Psi4 <http://psicode.org>`__ (licensed under GNU Lesser General Public License version 3) to interface with OpenFermion.

Installation
------------

To start using OpenFermion-Psi4, first install `OpenFermion <http://openfermion.org>`__ and
`Psi4 <http://psicode.org>`__. Then, clone this git repo, change directory to the top level folder and run:

.. code-block:: bash

  python -m pip install -e .

Alternatively, one can install using pip with the command:

.. code-block:: bash

  python -m pip install openfermionpsi4

Also be sure to take a look at the ipython notebook demos in the examples folder of this repository.

Authors
-------

`Ryan Babbush <http://ryanbabbush.com>`__ (Google),
`Jarrod McClean <http://jarrodmcclean.com>`__ (Google),
Ian Kivlichan (Harvard),
Damian Steiger (ETH Zurich),
Thomas Haner (ETH Zurich),
Craig Gidney (Google) and
Dave Bacon (Google).

Disclaimer
----------
Copyright 2017 The OpenFermion Developers.
This is not an official Google product.
