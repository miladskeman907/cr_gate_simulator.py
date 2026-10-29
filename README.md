# Quantum Surface Code Decoder & Noise Simulator

A high-performance, research-grade quantum error correction (QEC) simulation pipeline implementing the rotated memory-Z surface code. This project leverages **Stim** for ultra-fast stabilizer circuit generation and detector error model extraction, combined with **PyMatching** for efficient Minimum-Weight Perfect Matching (MWPM) decoding.

## 🔬 Core Features
- **Surface Code Generation:** Builds standard rotated memory-Z surface code circuits for arbitrary code distances ($d$) and error rounds ($r$).
- **Realistic Noise Injection:** Incorporates physical depolarizing noise after Clifford gates, bit-flips on resets, and measurement error probabilities.
- **Detector Error Model (DEM):** Automatically extracts logical observables and detector error graphs for accurate decoding.
- **MWPM Decoding Pipeline:** Utilizes PyMatching to process syndromes, predict logical errors, and compute the precise **Logical Failure Rate**.

## 🛠️ Simulation Workflow
1. Circuit creation using `stim.Circuit.generated` with configurable noise parameters ($p$).
2. Syndrome extraction and sampling via compiled detector samplers.
3. Maximum-likelihood decoding via Minimum-Weight Perfect Matching (MWPM).
4. Statistical evaluation of logical error rates across varying physical error rates.

## 🚀 Quick Start
Run the surface code simulation pipeline locally:
```bash
python decoder.py
