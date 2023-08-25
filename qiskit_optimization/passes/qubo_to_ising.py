# This code is part of Qiskit.
#
# (C) Copyright IBM 2023
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
QUBO workflow
"""
from qiskit_optimization import QuadraticProgram
from qiskit.quantum_info import SparsePauliOp

from .validation import validate_output_type
from ..fulqrum import PropertySet


class QUBO2Ising:
    """A mapping of `QuadraticProgram` for a QUBO problem to a Ising Hamiltonian
    in `SparsePauliOp` format
    """
    def __init__(self):
        self.input_types = (QuadraticProgram, )
        self.output_types = (SparsePauliOp, )
        self.property_set = PropertySet()

    @validate_output_type
    def run(self, program):
        if not isinstance(program, self.input_types):
            raise TypeError(f"Program is invalid input type, must be one of {self.input_types}")
        ising, constant = program.to_ising(opflow=False)
        return ising + SparsePauliOp.from_list([("I"*ising.num_qubits, constant)])
