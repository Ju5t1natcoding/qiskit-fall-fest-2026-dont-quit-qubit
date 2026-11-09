# The Quantum Clock of Iași

> A story-driven quantum computing challenge developed for **Qiskit Fall Fest Iași 2026** by Team **Don't quit, qubit!**

## Overview

**The Quantum Clock of Iași** (*Ceasul Cuantic al Iașului*) is an educational quantum computing challenge built around a fictional story set in Iași, Romania.

In the year 2036, the city's quantum network processor, **QIași-1**, has been sabotaged. Its qubits are out of calibration, connections between nodes have been disrupted, and the key needed to restart the system has been hidden somewhere in the city.

As members of the Intervention Team, participants must investigate the incident, repair the quantum network, uncover the identity of the mysterious "Shadow", and restore the clock.

The challenge consists of **six levels and eight bells**, each representing an important milestone in the recovery process. Its tasks introduce fundamental quantum computing concepts and gradually progress towards quantum communication, quantum algorithms, and experiments on real quantum hardware.

The story takes participants through several recognizable locations in Iași, connecting quantum computing concepts with the city's landmarks.

## Learning Path

| Level | Name | Main Topics |
|---|---|---|
| 0 | First Steps | Python, Qiskit, qubits, superposition, measurement, quantum gates and entanglement |
| 1 | The Heart of the Clock | Qubit calibration, rotation gates and probability control |
| 2 | The Sabotaged Component | Matrix representations of quantum gates, phase and black-box gate identification |
| 3 | The Copou Connection | Bell states, entanglement, superdense coding and quantum teleportation |
| 4 | The Asachi Key | XOR encryption, the BB84 quantum key distribution protocol and eavesdropper detection |
| 5 | The Hideout | Grover's search algorithm, quantum oracles and amplitude amplification |
| 6 | The Bells | Real IBM quantum hardware, quantum noise and readout error mitigation |

Each level combines explanations, programming exercises, verification tasks and optional bonus challenges.

## Repository Structure

```text
.
├── Auxiliary Code/
│   └── produs_matrici.cpp
│
├── Final Project/
│   └── LINK CANVA.docx
│
├── Given Resources/
│   ├── Deschiderea provocării — slide-uri.pdf
│   ├── Nivelul_0_Primii_pasi.ipynb
│   ├── Nivelul_1_Inima_ceasului.ipynb
│   ├── Nivelul_2_Piesa_sabotata.ipynb
│   ├── Nivelul_3_Legatura_Copou.ipynb
│   ├── Nivelul_4_Cheia_Asachi.ipynb
│   ├── Nivelul_5_Ascunzatoarea.ipynb
│   ├── Nivelul_6_Clopotele.ipynb
│   └── ceas_cuantic.py
│
├── Preparation/
│   ├── Nivelul_0_Primii_pasi.ipynb
│   └── Nivelul_0_Primii_pasi___worked_on.ipynb
│
└── Solutions/
    ├── Nivelul_1_Inima_ceasului.ipynb
    ├── Nivelul_2_Piesa_sabotata.ipynb
    ├── Nivelul_3_Legatura_Copou.ipynb
    ├── Nivelul_4_Cheia_Asachi.ipynb
    ├── Nivelul_5_Ascunzatoarea.ipynb
    └── Nivelul_6_Clopotele.ipynb
```

### Directory Guide

- **`Given Resources/`** — Challenge materials, introductory notebooks, the original level notebooks and the supporting Python library.
- **`Preparation/`** — Introductory exercises and a worked-on version used during preparation.
- **`Solutions/`** — Our implementations and solutions for the six challenge levels.
- **`Auxiliary Code/`** — A C++ implementation of complex numbers and matrix operations, including tensor products.
- **`Final Project/`** — A reference document for the team's final presentation.

## Technologies

The project uses:

- **Python** — Main programming language for the quantum computing exercises.
- **Qiskit** — Quantum circuit construction, simulation and execution.
- **NumPy** — Numerical computations and matrix operations.
- **Matplotlib** — Visualizing measurement results, probabilities and quantum states.
- **Jupyter Notebooks** — Interactive learning materials and challenge solutions.
- **C++** — Auxiliary implementation of complex numbers and matrix operations.

The final level additionally uses **Qiskit IBM Runtime** to submit circuits to real IBM quantum hardware.

## Getting Started

A Python environment with Jupyter, Qiskit, NumPy and Matplotlib is required.

A basic environment can be prepared using:

```bash
python -m pip install jupyterlab numpy matplotlib qiskit qiskit-ibm-runtime
```

Start JupyterLab from the repository directory:

```bash
jupyter lab
```

For the intended learning progression:

1. Start with `Nivelul_0_Primii_pasi.ipynb`.
2. Read the provided introductory materials.
3. Work through the challenge notebooks in numerical order, from Level 1 to Level 6.
4. Consult the corresponding notebooks in `Solutions/` when reviewing the implementations.

The challenge notebooks use `ceas_cuantic.py` for communication with the organizers' verification server. Make sure this file is accessible through Python's import path when running notebooks from a different directory.

Some challenge verification tasks depend on the availability of the organizers' server. The final hardware experiments also require an appropriately configured IBM Quantum account and access to a real quantum backend.

## Final Presentation

The repository includes a presentation reference document:

[`Final Project/project_link_CANVA.txt`](Final%20Project/project_link_CANVA.txt)

## Team

**Team Name:** *Don't quit, qubit!*

Individual team members and their contributions will be listed here after they have been confirmed by each member.

## Event

**Qiskit Fall Fest Iași 2026**

Faculty of Automatic Control and Computer Engineering, TUIASI  
Iași, Romania

---

*Exploring quantum computing, one qubit at a time.*
