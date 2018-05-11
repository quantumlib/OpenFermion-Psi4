#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import psi4
import pubchempy as pcp


def parse_sdf_geometry(geom, n_atoms):
    opf_geom = []
    vec = geom.split('\n')[2:2 + n_atoms]

    for i in range(len(vec)):
        x = vec[i].split()[:4]
        tup = tuple([float(x) for x in x[1:]])
        atom = x[0].lower().capitalize()
        opf_geom.append((atom, tup))

    return opf_geom


def parse_psi4_geometry(geom, n_atoms):
    opf_geom = []
    vec = geom.split('\n')[2:2 + n_atoms]

    for i in range(len(vec)):
        x = vec[i].split()[:4]
        tup = tuple([float(x) for x in x[:3]])
        atom = x[3].lower().capitalize()
        opf_geom.append((atom, tup))
    return opf_geom


def extract(name_):
    """Function to create MolecularData geometry from the molecule's name.

    Args:
        name_: a string giving the molecule's name as required by the PubChem
            database. This can be quite flexible, e.g.: 'water' or 'H2O' or
            or 'dihyrogen oxide' for the same molecule.

    Returns:
        opf_geom: a list of tuples giving the coordinates of each atom with
        distances in Angstrom. Example is:
        [('O', (0.0, 0.0, -0.066779921147764)),
        ('H', (0.0, -0.763469300299257, 0.529922904804988)),
        ('H', (-0.0, 0.763469300299257, 0.529922904804988))]
    """
    try:
        name = pcp.get_compounds(name_, 'name', record_type='3d')[0]
        mlc = psi4.geometry("""
pubchem:{}
""".format(name_))
        mlc = mlc.create_psi4_string_from_molecule()
        n_atoms = len(name.atoms)
        opf_geom = parse_sdf_geometry(mlc, n_atoms)
        print('3D compound found.')

    except IndexError:
        try:
            name = pcp.get_compounds(name_, 'name', record_type='2d')[0]
            n_atoms = len(name.atoms)
            mlc = pcp.get_sdf(name.cid)
            opf_geom = parse_psi4_geometry(mlc, n_atoms)
            print('2D compound found.')
        except IndexError:
            opf_geom = 0
            print("Unable to find molecule in the PubChem database.")

    return opf_geom
