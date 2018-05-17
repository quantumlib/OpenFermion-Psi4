# OpenFermion plugin to interface with Psi4.
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

"""Helper functions for parsing data files of different types."""
from __future__ import absolute_import

import numpy

from openfermion.ops import InteractionOperator


def unpack_spatial_rdm(one_rdm_a,
                       one_rdm_b,
                       two_rdm_aa,
                       two_rdm_ab,
                       two_rdm_bb):
    """
    Covert from spin compact spatial format to spin-orbital format for RDM.

    Note: the compact 2-RDM is stored as follows where A/B are spin up/down:
    RDM[pqrs] = <| a_{p, A}^\dagger a_{r, A}^\dagger a_{q, A} a_{s, A} |>
      for 'AA'/'BB' spins.
    RDM[pqrs] = <| a_{p, A}^\dagger a_{r, B}^\dagger a_{q, B} a_{s, A} |>
      for 'AB' spins.

    Args:
        one_rdm_a: 2-index numpy array storing alpha spin
            sector of 1-electron reduced density matrix.
        one_rdm_b: 2-index numpy array storing beta spin
            sector of 1-electron reduced density matrix.
        two_rdm_aa: 4-index numpy array storing alpha-alpha spin
            sector of 2-electron reduced density matrix.
        two_rdm_ab: 4-index numpy array storing alpha-beta spin
            sector of 2-electron reduced density matrix.
        two_rdm_bb: 4-index numpy array storing beta-beta spin
            sector of 2-electron reduced density matrix.

    Returns:
        one_rdm: 2-index numpy array storing 1-electron density matrix
            in full spin-orbital space.
        two_rdm: 4-index numpy array storing 2-electron density matrix
            in full spin-orbital space.
    """
    # Initialize RDMs.
    n_orbitals = one_rdm_a.shape[0]
    n_qubits = 2 * n_orbitals
    one_rdm = numpy.zeros((n_qubits, n_qubits))
    two_rdm = numpy.zeros((n_qubits, n_qubits,
                           n_qubits, n_qubits))

    # Unpack compact representation.
    for p in range(n_orbitals):
        for q in range(n_orbitals):

            # Populate 1-RDM.
            one_rdm[2 * p, 2 * q] = one_rdm_a[p, q]
            one_rdm[2 * p + 1, 2 * q + 1] = one_rdm_b[p, q]

            # Continue looping to unpack 2-RDM.
            for r in range(n_orbitals):
                for s in range(n_orbitals):

                    # Handle case of same spin.
                    two_rdm[2 * p, 2 * q, 2 * r, 2 * s] = (
                        two_rdm_aa[p, r, q, s])
                    two_rdm[2 * p + 1, 2 * q + 1, 2 * r + 1, 2 * s + 1] = (
                        two_rdm_bb[p, r, q, s])

                    # Handle case of mixed spin.
                    two_rdm[2 * p, 2 * q + 1, 2 * r, 2 * s + 1] = (
                        two_rdm_ab[p, r, q, s])
                    two_rdm[2 * p, 2 * q + 1, 2 * r + 1, 2 * s] = (
                        -1. * two_rdm_ab[p, s, q, r])
                    two_rdm[2 * p + 1, 2 * q, 2 * r + 1, 2 * s] = (
                        two_rdm_ab[q, s, p, r])
                    two_rdm[2 * p + 1, 2 * q, 2 * r, 2 * s + 1] = (
                        -1. * two_rdm_ab[q, r, p, s])

    # Map to physicist notation and return.
    two_rdm = numpy.einsum('pqsr', two_rdm)
    return one_rdm, two_rdm


def parse_psi4_ccsd_amplitudes(number_orbitals,
                               n_alpha_electrons, n_beta_electrons,
                               psi_filename):
    """Parse coupled cluster singles and doubles amplitudes from psi4 file.

    Args:
      number_orbitals(int): Number of total spin orbitals in the system
      n_alpha_electrons(int): Number of alpha electrons in the system
      n_beta_electrons(int): Number of beta electrons in the system
      psi_filename(str): Filename of psi4 output file

    Returns:
      molecule(InteractionOperator): Molecular Operator instance holding ccsd
        amplitudes

    """
    output_buffer = [line for line in open(psi_filename)]

    T1IA_index = None
    T1ia_index = None
    T2IJAB_index = None
    T2ijab_index = None
    T2IjAb_index = None

    # Find Start Indices
    for i, line in enumerate(output_buffer):
        if ('Largest TIA Amplitudes:' in line):
            T1IA_index = i

        elif ('Largest Tia Amplitudes:' in line):
            T1ia_index = i

        elif ('Largest TIJAB Amplitudes:' in line):
            T2IJAB_index = i

        elif ('Largest Tijab Amplitudes:' in line):
            T2ijab_index = i

        elif ('Largest TIjAb Amplitudes:' in line):
            T2IjAb_index = i

    T1IA_Amps = []
    T1ia_Amps = []

    T2IJAB_Amps = []
    T2ijab_Amps = []
    T2IjAb_Amps = []

    # Read T1's
    if (T1IA_index is not None):
        for line in output_buffer[T1IA_index + 1:]:
            ivals = line.split()
            if not ivals:
                break
            T1IA_Amps.append([int(ivals[0]), int(ivals[1]), float(ivals[2])])

    if (T1ia_index is not None):
        for line in output_buffer[T1ia_index + 1:]:
            ivals = line.split()
            if not ivals:
                break
            T1ia_Amps.append([int(ivals[0]), int(ivals[1]), float(ivals[2])])

    # Read T2's
    if (T2IJAB_index is not None):
        for line in output_buffer[T2IJAB_index + 1:]:
            ivals = line.split()
            if not ivals:
                break
            T2IJAB_Amps.append([int(ivals[0]), int(ivals[1]),
                                int(ivals[2]), int(ivals[3]),
                                float(ivals[4])])

    if (T2ijab_index is not None):
        for line in output_buffer[T2ijab_index + 1:]:
            ivals = line.split()
            if not ivals:
                break
            T2ijab_Amps.append([int(ivals[0]), int(ivals[1]),
                                int(ivals[2]), int(ivals[3]),
                                float(ivals[4])])

    if (T2IjAb_index is not None):
        for line in output_buffer[T2IjAb_index + 1:]:
            ivals = line.split()
            if not ivals:
                break
            T2IjAb_Amps.append([int(ivals[0]), int(ivals[1]),
                                int(ivals[2]), int(ivals[3]),
                                float(ivals[4])])

    # Determine if calculation is restricted / closed shell or otherwise
    restricted = T1ia_index is None and T2ijab_index is None

    # Store amplitudes with spin-orbital indexing, including appropriate
    # symmetry
    single_amplitudes = numpy.zeros((number_orbitals, ) * 2)
    double_amplitudes = numpy.zeros((number_orbitals, ) * 4)

    # Define local helper routines for clear indexing of orbitals
    def alpha_occupied(i):
        return 2 * i

    def alpha_unoccupied(i):
        return 2 * (i + n_alpha_electrons)

    def beta_occupied(i):
        return 2 * i + 1

    def beta_unoccupied(i):
        return 2 * (i + n_beta_electrons) + 1

    # Store singles
    for entry in T1IA_Amps:
        i, a, value = entry
        single_amplitudes[alpha_unoccupied(a),
                          alpha_occupied(i)] = value
        if (restricted):
            single_amplitudes[beta_unoccupied(a),
                              beta_occupied(i)] = value

    for entry in T1ia_Amps:
        i, a, value = entry
        single_amplitudes[beta_unoccupied(a),
                          beta_occupied(i)] = value

    # Store doubles, include factor of 1/2 for convention
    for entry in T2IJAB_Amps:
        i, j, a, b, value = entry
        double_amplitudes[alpha_unoccupied(a),
                          alpha_occupied(i),
                          alpha_unoccupied(b),
                          alpha_occupied(j)] = value / 2.
        if (restricted):
            double_amplitudes[beta_unoccupied(a),
                              beta_occupied(i),
                              beta_unoccupied(b),
                              beta_occupied(j)] = value / 2.

    for entry in T2ijab_Amps:
        i, j, a, b, value = entry
        double_amplitudes[beta_unoccupied(a),
                          beta_occupied(i),
                          beta_unoccupied(b),
                          beta_occupied(j)] = value / 2.

    for entry in T2IjAb_Amps:
        i, j, a, b, value = entry
        double_amplitudes[alpha_unoccupied(a),
                          alpha_occupied(i),
                          beta_unoccupied(b),
                          beta_occupied(j)] = value / 2.

        if (restricted):
            double_amplitudes[beta_unoccupied(a),
                              beta_occupied(i),
                              alpha_unoccupied(b),
                              alpha_occupied(j)] = value / 2.

    return single_amplitudes, double_amplitudes
