# Transmon Two-Qubit Cross-Resonance (CR) Gate & Parasitic ZZ Simulator

A quantum hardware simulation suite designed to model coupled superconducting transmon qubits, analyze Cross-Resonance (CR) gate dynamics, and calculate parasitic ZZ crosstalk interactions.

## 🔬 Theoretical Framework

### 1. Coupled Transmon Hamiltonian
The composite system of two transmon qubits coupled via a central bus/resonator is modeled in the basis of charge states including anharmonicity and coupling terms:

$$H_{sys} = \sum_{i=1}^{2} \left( \omega_i a_i^\dagger a_i + \frac{\alpha_i}{2} a_i^\dagger a_i^\dagger a_i a_i \right) + g (a_1 a_2^\dagger + a_1^\dagger a_2)$$

### 2. Parasitic ZZ Crosstalk ($\zeta_{ZZ}$)
Quantifies the unwanted static frequency shifts between qubits due to higher-level leakage and dispersive shifts:

$$\zeta_{ZZ} \approx \frac{2 g^2 (\alpha_1 + \alpha_2)}{\Delta^2 - (\alpha_1 + \alpha_2)^2}$$

Where $\Delta = \omega_1 - \omega_2$ is the qubit-qubit detuning.

## 🛠️ Tech Stack
* **Python**
* **NumPy & SciPy** (Matrix diagonalization, tensor products, & analytical approximations)
* **Matplotlib** (Crosstalk and Hamiltonian spectrum visualization)

## 📄 License
This project is open-source under the [MIT License](LICENSE).
