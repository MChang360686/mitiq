---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.4
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Measuring Resources Required

Measuring the cost to run a quantum error mitigation (QEM) experiement would be ideally done in dollars.  This is difficult due to provider opacity, so cost should be measured by 

- the number of circuits the technique uses
- the number of additional gates

This can be done by using mitiq's two stage application of ```mitiq.xyz.construct_circuits``` and ```mitiq.xyz.combine_results```.  The example below demonstrates this using Layerwise Richardson Extrapolation (LRE) applied to a Greenberger-Horne-Zeilinger (GHZ) circuit.

## Measuring the number of circuits required

After using ```construct_circuits``` for a technique, a list of folded circuits should be returned.  The length of this list is the number of circuits required.

```{code-cell} ipython3
import cirq
from mitiq.benchmarks import generate_ghz_circuit
from mitiq import lre

# Generate GHZ circuit
num_qubits = 3
circuit = generate_ghz_circuit(num_qubits)

def count_gates(circ):
    return sum(1 for _ in circ.all_operations())

original_gate_count = count_gates(circuit)
print(f"Original circuit gate count: {original_gate_count}")

# Fold gates using construct_circuits
degree = 2
fold_multiplier = 2  # scaling parameter
folded_circuits = lre.construct_circuits(circuit, degree, fold_multiplier)

print(f"Number of circuits required (folded): {len(folded_circuits)}")

# Create simulator and run circuit to find mitigated value
simulator = cirq.Simulator()

def execute_expectation(circuit):
    qubits = circuit.all_qubits()
    observable = cirq.Z(list(qubits)[0])
    result = simulator.simulate_expectation_values(circuit, observables=[observable])
    return result[0].real

results = [execute_expectation(c) for c in folded_circuits]

mitigated_value = lre.combine_results(results, circuit, degree, fold_multiplier)
print(mitigated_value)
```


## Measuring the number of additional gates

The number of additional gates can be measured by comparing the original circuit to each folded circuit and computing the difference.

```{code-cell} ipython3
import cirq
from mitiq.benchmarks import generate_ghz_circuit
from mitiq import lre

# Generate GHZ circuit
num_qubits = 3
circuit = generate_ghz_circuit(num_qubits)

# Return sum of gates in circuit circ
def count_gates(circ):
    return sum(1 for _ in circ.all_operations())

# Count the original number of gates
original_gate_count = count_gates(circuit)
print(f"Original circuit gate count: {original_gate_count}")

# Compare the number of folded gates to the original count
for i, folded in enumerate(folded_circuits, start=1):
    gate_count = count_gates(folded)
    added_gates = gate_count - original_gate_count
    print(f"Folded Circuit {i}: {gate_count} extra gates")

# Create simulator and run circuit to find mitigated value
simulator = cirq.Simulator()

def execute_expectation(circuit):
    qubits = circuit.all_qubits()
    observable = cirq.Z(list(qubits)[0])
    result = simulator.simulate_expectation_values(circuit, observables=[observable])
    return result[0].real

results = [execute_expectation(c) for c in folded_circuits]

mitigated_value = lre.combine_results(results, circuit, degree, fold_multiplier)
print(mitigated_value)
```