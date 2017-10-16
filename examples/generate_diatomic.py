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

from openfermion.hamiltonians import MolecularData

from openfermionpsi4 import run_psi4

if __name__ == '__main__':

    # Set chemical parameters.
    element_names = ['H', 'H']
    basis = 'sto-3g'
    charge = 0
    multiplicity = 1

    # Single point at equilibrium for testing
    spacings = [0.7414]

    # Add points for a full dissociation curve from 0.1 to 3.0 angstroms
    spacings += [0.1 * r for r in range(1, 31)]

    # Set run options
    run_scf = 1
    run_mp2 = 1
    run_cisd = 1
    run_ccsd = 1
    run_fci = 1
    verbose = 1
    tolerate_error = 1

    # Run Diatomic Curve
    for spacing in spacings:
        description = "{}".format(spacing)
        geometry = [[element_names[0], [0, 0, 0]],
                    [element_names[1], [0, 0, spacing]]]
        molecule = MolecularData(geometry,
                                 basis,
                                 multiplicity,
                                 charge,
                                 description)

        molecule = run_psi4(molecule,
                            run_scf=run_scf,
                            run_mp2=run_mp2,
                            run_cisd=run_cisd,
                            run_ccsd=run_ccsd,
                            run_fci=run_fci,
                            verbose=verbose,
                            tolerate_error=tolerate_error)
        molecule.save()

    # Run Li H single point
    description = "1.45"
    geometry = [['Li', [0, 0, 0]],
                ['H', [0, 0, 1.45]]]
    molecule = MolecularData(geometry,
                             basis,
                             multiplicity,
                             charge,
                             description)

    molecule = run_psi4(molecule,
                        run_scf=run_scf,
                        run_mp2=run_mp2,
                        run_cisd=run_cisd,
                        run_ccsd=run_ccsd,
                        run_fci=run_fci,
                        verbose=verbose,
                        tolerate_error=tolerate_error)
    molecule.save()
