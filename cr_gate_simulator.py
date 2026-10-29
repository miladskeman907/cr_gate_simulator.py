

import numpy as np


class QuantumGate:
    VALID_GATES = {"H", "X", "Y", "Z", "CNOT", "RZ"}

    def __init__(self, name, qubits, params=None):
        self.name = name.upper()
        self.qubits = tuple(qubits)
        self.params = params

    def __repr__(self):
        return (
            f"Gate({self.name}, "
            f"qubits={self.qubits}, params={self.params})"
        )


class QuantumCircuitOptimizer:
    def __init__(self, num_qubits):
        if not isinstance(num_qubits, int) or num_qubits <= 0:
            raise ValueError("num_qubits must be a positive integer")

        self.num_qubits = num_qubits
        self.gates = []

    def add_gate(self, name, qubits, params=None):
        gate = QuantumGate(name, qubits, params)
        self._validate_gate(gate)
        self.gates.append(gate)

    def _validate_gate(self, gate):
        if gate.name not in QuantumGate.VALID_GATES:
            raise ValueError(f"Unsupported gate: {gate.name}")

        expected = 2 if gate.name == "CNOT" else 1

        if len(gate.qubits) != expected:
            raise ValueError(
                f"{gate.name} requires {expected} qubit(s)"
            )

        if len(set(gate.qubits)) != len(gate.qubits):
            raise ValueError("A gate cannot use the same qubit twice")

        for q in gate.qubits:
            if not isinstance(q, int):
                raise ValueError("Qubit index must be an integer")

            if not 0 <= q < self.num_qubits:
                raise ValueError(f"Invalid qubit index: {q}")

        if gate.name == "RZ":
            if gate.params is None:
                raise ValueError("RZ requires an angle")

            if not np.isscalar(gate.params):
                raise ValueError("RZ angle must be a scalar")

            if not np.isfinite(gate.params):
                raise ValueError("RZ angle must be finite")

    @staticmethod
    def _same_cnot(gate1, gate2):
        return (
            gate1.name == "CNOT"
            and gate2.name == "CNOT"
            and gate1.qubits == gate2.qubits
        )

    @staticmethod
    def _same_rz_qubit(gate1, gate2):
        return (
            gate1.name == "RZ"
            and gate2.name == "RZ"
            and gate1.qubits == gate2.qubits
        )

    def optimize(self):
        print(f"Initial gate count: {len(self.gates)}")

        optimized = []
        i = 0

        while i < len(self.gates):
            current = self.gates[i]

            # Cancel adjacent identical CNOT gates.
            if i + 1 < len(self.gates):
                next_gate = self.gates[i + 1]

                if self._same_cnot(current, next_gate):
                    print(f"Cancelled CNOT pair: {current.qubits}")
                    i += 2
                    continue

                # Cancel adjacent inverse RZ rotations.
                if self._same_rz_qubit(current, next_gate):
                    angle_sum = current.params + next_gate.params

                    if np.isclose(
                        angle_sum,
                        0.0,
                        atol=1e-10
                    ):
                        print(f"Cancelled RZ pair: {current.qubits}")
                        i += 2
                        continue

            # Look for matching CNOT gates separated by
            # gates acting on completely unrelated qubits.
            if current.name == "CNOT":
                j = i + 1

                while j < len(self.gates):
                    candidate = self.gates[j]

                    if self._same_cnot(current, candidate):
                        print(
                            f"Cancelled separated CNOT pair: "
                            f"{current.qubits}"
                        )

                        # Preserve the unrelated gates between
                        # the two CNOT gates.
                        optimized.extend(self.gates[i + 1:j])

                        i = j + 1
                        break

                    # Only commute past gates that act on
                    # neither CNOT qubit.
                    if set(candidate.qubits).isdisjoint(
                        current.qubits
                    ):
                        j += 1
                    else:
                        break

                else:
                    optimized.append(current)
                    i += 1
                    continue

                continue

            optimized.append(current)
            i += 1

        self.gates = optimized

        print(f"Final gate count: {len(self.gates)}")
        return self.gates

    def get_circuit_depth(self):
        """
        Calculate logical circuit depth.

        Gates acting on disjoint qubits may share a layer.
        """
        qubit_depth = [0] * self.num_qubits

        for gate in self.gates:
            layer = max(
                qubit_depth[q] for q in gate.qubits
            ) + 1

            for q in gate.qubits:
                qubit_depth[q] = layer

        return max(qubit_depth, default=0)

    def print_circuit(self):
        for index, gate in enumerate(self.gates):
            print(f"{index}: {gate}")


if __name__ == "__main__":
    qc = QuantumCircuitOptimizer(num_qubits=3)

    qc.add_gate("H", (0,))
    qc.add_gate("CNOT", (0, 1))
    qc.add_gate("CNOT", (0, 1))

    qc.add_gate("RZ", (1,), params=np.pi / 4)
    qc.add_gate("RZ", (1,), params=-np.pi / 4)

    qc.add_gate("CNOT", (1, 2))
    qc.add_gate("H", (0,))
    qc.add_gate("CNOT", (1, 2))

    print("\n--- Before Optimization ---")
    print("Gate count:", len(qc.gates))
    print("Circuit depth:", qc.get_circuit_depth())

    qc.optimize()

    print("\n--- After Optimization ---")
    print("Gate count:", len(qc.gates))
    print("Circuit depth:", qc.get_circuit_depth())

    print("\nOptimized circuit:")
    qc.print_circuit()
