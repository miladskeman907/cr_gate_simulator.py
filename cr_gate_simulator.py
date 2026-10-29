
import numpy as np
import matplotlib.pyplot as plt

def simulate_cr_dynamics(drive_amplitude, coupling_g, detuning, time_steps):
    """
    Simulates Cross-Resonance (CR) gate drive dynamics and parasitic ZZ interaction.
    """
    times = np.linspace(0, time_steps, 200)
    # Effective Rabi frequency for target qubit driven via control
    omega_eff = np.sqrt((drive_amplitude * coupling_g / detuning)**2 + (coupling_g)**2)
    
    # Population oscillation of target qubit
    target_excitation = np.sin(omega_eff * times)**2
    zz_phase_shift = coupling_g * np.cos(times)
    
    return times, target_excitation, zz_phase_shift

# Generate simulation data for Transmon qubits
t, excitation, zz_shift = simulate_cr_dynamics(drive_amplitude=0.05, coupling_g=0.02, detuning=0.8, time_steps=50)

# Plotting the Quantum Hardware Dynamics
plt.figure(figsize=(10, 5))
plt.plot(t, excitation, label='Target Qubit State Population (CR Drive)', color='#1f77b4', linewidth=2)
plt.plot(t, zz_shift, label='Parasitic ZZ Crosstalk Phase Shift', color='#ff7f0e', linestyle='--', linewidth=1.5)

plt.title('Transmon Two-Qubit Cross-Resonance (CR) Gate Dynamics', fontsize=12, fontweight='bold')
plt.xlabel('Time (ns)', fontsize=10)
plt.ylabel('Amplitude / Population', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right')
plt.tight_layout()

# Save image for repository documentation
plt.savefig('cr_gate_simulation_plot.png', dpi=300)
print("Quantum CR gate simulation complete. Plot saved successfully.")
