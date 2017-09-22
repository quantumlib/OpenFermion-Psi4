# OpenFermion plugin to interface with Psi4
# Copyright 2017 The OpenFermion Developers.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This is a simple script for generating data."""
import os

from openfermion.utils import (make_atomic_ring,
                               make_atom,
                               MolecularData,
                               periodic_table)

from openfermionpsi4 import run_psi4


if __name__ == '__main__':

    # Set chemical parameters.
    basis = 'sto-3g'
    max_electrons = 10
    spacing = 0.7414
    compute_elements = 0

    # Select calculations.
    force_recompute = 1
    run_scf = 1
    run_mp2 = 1
    run_cisd = 1
    run_ccsd = 1
    run_fci = 1
    verbose = 1
    tolerate_error = 1

    # Generate data.
    for n_electrons in range(2, max_electrons + 1):

        # Initialize.
        if compute_elements:
            atomic_symbol = periodic_table[n_electrons]
            molecule = make_atom(atomic_symbol, basis)
        else:
            molecule = make_atomic_ring(n_electrons, spacing, basis)
        if os.path.exists(molecule.filename + '.hdf5'):
            molecule.load()

        # To run or not to run.
        if run_scf and not molecule.hf_energy:
            run_job = 1
        elif run_mp2 and not molecule.mp2_energy:
            run_job = 1
        elif run_cisd and not molecule.cisd_energy:
            run_job = 1
        elif run_ccsd and not molecule.ccsd_energy:
            run_job = 1
        elif run_fci and not molecule.fci_energy:
            run_job = 1
        else:
            run_job = force_recompute

        # Run.
        if run_job:
            molecule = run_psi4(molecule,
                                run_scf=run_scf,
                                run_mp2=run_mp2,
                                run_cisd=run_cisd,
                                run_ccsd=run_ccsd,
                                run_fci=run_fci,
                                verbose=verbose,
                                tolerate_error=tolerate_error)
            molecule.save()
