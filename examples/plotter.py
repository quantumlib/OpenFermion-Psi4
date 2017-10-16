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

"""These functions compare properties of different molecules."""
import numpy
import warnings

from openfermion.hamiltonians import make_atomic_ring, MolecularData

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import pylab


def latex_name(molecule):
    """Write the name of the molecule in LaTeX.

    Returns:
        name: A string giving the name in LaTeX.
    """
    # Get sorted atom vector.
    atoms = [item[0] for item in molecule.geometry]
    atom_charge_info = [(atom, atoms.count(atom)) for atom in set(atoms)]
    sorted_info = sorted(atom_charge_info,
                         key=lambda atom: molecular_data.
                         _PERIODIC_HASH_TABLE[atom[0]])

    # Name molecule and return.
    name = '{}$_{}$'.format(sorted_info[0][0], sorted_info[0][1])
    for info in sorted_info[1::]:
        name += '{}$_{}$'.format(info[0], info[1])
    return name


# Run.
if __name__ == '__main__':

    # Set plot parameters.
    pylab.rcParams['text.usetex'] = True
    pylab.rcParams['text.latex.unicode'] = True
    pylab.rc('text', usetex=True)
    pylab.rc('font', family='sans=serif')
    marker_size = 6
    line_width = 2
    axis_size = 12
    font_size = 16
    x_log = 0
    y_log = 0

    # Set chemical series parameters.
    max_electrons = 10
    spacing = 0.7414
    basis = 'sto-3g'

    # Get chemical series.
    molecular_series = []
    for n_electrons in range(2, max_electrons + 1):
        molecule = make_atomic_ring(n_electrons, spacing, basis)
        molecule.load()
        molecular_series += [molecule]

    # Get plot data.
    x_values = []
    y_values = []
    for molecule in molecular_series:

        # x-axis.
        x_label = 'Number of Electrons'
        x_values += [molecule.n_electrons]

        # y-axis.
        y_label = 'MP2 Energy'
        y_values += [molecule.mp2_energy]

        # Print.
        print('\n{} for {} = {}.'.format(x_label, molecule.name, x_values[-1]))
        print('{} for {} = {}.'.format(y_label, molecule.name, y_values[-1]))

    # Plot.
    pylab.figure(0)
    pylab.plot(x_values, y_values, lw=0, marker='o')

    # Set log scales.
    if y_log:
        pylab.yscale('log')
    if x_log:
        pylab.xscale('log')

    # Finish making the plot.
    pylab.xticks(size=axis_size)
    pylab.yticks(size=axis_size)
    pylab.xlabel(r'%s' % x_label, fontsize=font_size)
    pylab.ylabel(r'%s' % y_label, fontsize=font_size)
    pylab.show()
