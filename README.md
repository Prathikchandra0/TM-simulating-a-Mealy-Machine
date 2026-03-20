# Mealy Machine Turing Machine Simulator

## Overview

This project implements a **complete simulation** of a **Mealy Machine using a Turing Machine (TM) approach**, suitable for a Theory of Computation course as a complex engineering problem.

### What is a Mealy Machine?

A **Mealy Machine** is a finite state machine (FSM) where:
- **Output depends on both the current state AND the input symbol**
- **Output is produced during transitions** (not in states)
- **Transition function**: δ(state, input) → (next_state, output)
- **Advantage**: More expressive than Moore machines; compact representation

Example: A vending machine that outputs change based on current balance and coin inserted.

### What is a Turing Machine?

A **Turing Machine (TM)** is an abstract computational model with:
- **Infinite tape** divided into cells
- **Read/write head** that can move left or right
- **State machine** controlling transitions
- **Equivalent power** to any real computer (Church-Turing Thesis)

### Why Simulate Mealy Machines with Turing Machines?

This project demonstrates:
1. **Hierarchy of Automata**: DFA → Mealy → TM
2. **Compatibility**: Finite automata can execute on more powerful models
3. **Encoding**: How to represent FSM transitions in TM notation
4. **Computation Theory**: Bridging finite and infinite computation

---

## Project Structure

```
.
├── src/                           # Core modules
│   ├── __init__.py
│   ├── tape.py                   # Tape abstraction
│   ├── mealy_machine.py          # Mealy Machine class
│   ├── turing_machine.py         # Turing Machine simulator
│   ├── config_loader.py          # JSON configuration loading
│   └── visualizer.py             # Trace visualization
├── machines/                      # Machine definitions (JSON)
│   ├── binary_incrementer.json
│   └── parity_checker.json
├── tests/                         # Test cases
│   └── test_examples.py
├── gui_simulator.py              # GUI application (Tkinter)
├── cli_simulator.py              # Command-line interface
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

---

## Core Components

### 1. Tape Class (`src/tape.py`)

Represents the **infinite tape** of the Turing Machine:
- Dynamic list implementation
- Read/write operations
- Head movement (Left, Right, Stay)
- Automatic expansion

```python
tape = Tape("10101")
tape.read()        # Returns '1'
tape.write('0')    # Write at current position
tape.move('R')     # Move head right
```

### 2. Mealy Machine Class (`src/mealy_machine.py`)

Defines the **finite state machine** to be simulated:
- States, input alphabet, output alphabet
- Transition function management
- Validation of transitions
- Transition table printing

```python
machine = MealyMachine(
    states={"q0", "q1"},
    input_alphabet={"0", "1"},
    output_alphabet={"0", "1"},
    initial_state="q0"
)
machine.add_transition("q0", "1", "q1", "0")
```

### 3. Turing Machine Class (`src/turing_machine.py`)

**Simulates** the Mealy Machine:
- Executes step-by-step transitions
- Maintains execution trace
- Accumulates output
- Manages tape head position

```python
tm = TuringMachine(mealy_machine)
tm.initialize("101")
output, success, status = tm.execute_full()
```

### 4. Configuration Loader (`src/config_loader.py`)

Loads/saves machine definitions from **JSON**:
- Flexible machine definition format
- Validation of configurations
- Easy sharing and testing

```python
machine = ConfigLoader.load_from_file("machines/parity_checker.json")
ConfigLoader.save_to_file(machine, "output.json", "My Machine")
```

### 5. Visualizer (`src/visualizer.py`)

Provides **multiple visualization formats**:
- Trace tables
- Step-by-step output
- State-output mappings
- Interactive simulation

---

## Machine Definition Format (JSON)

```json
{
  "name": "Example Machine",
  "description": "Machine description",
  "states": ["q0", "q1", "q2"],
  "input_alphabet": ["0", "1"],
  "output_alphabet": ["0", "1"],
  "initial_state": "q0",
  "blank_symbol": "#",
  "transitions": [
    {
      "from": "q0",
      "input": "1",
      "to": "q1",
      "output": "0"
    }
  ]
}
```

---

## Usage

### 1. Command-Line Interface

**Without arguments** (runs demo):
```bash
python cli_simulator.py
```

**With a specific machine and input**:
```bash
python cli_simulator.py machines/parity_checker.json "11010"
```

**Verbose mode** (detailed trace):
```bash
python cli_simulator.py machines/parity_checker.json "11010" --verbose
```

**Interactive mode** (step-by-step):
```bash
python cli_simulator.py machines/parity_checker.json "11010" --interactive
```

### 2. Graphical User Interface

```bash
python gui_simulator.py
```

This launches a **Tkinter-based GUI** with:
- Machine loading from files or presets
- Input specification
- Run, interactive, or step-by-step modes
- Execution trace visualization
- Built-in documentation

### 3. Python API

```python
from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader

# Load machine
machine = ConfigLoader.load_from_file("machines/parity_checker.json")

# Create TM simulator
tm = TuringMachine(machine)

# Initialize with input
tm.initialize("11010")

# Execute step-by-step
is_halted, status = tm.execute_step()

# Or execute to completion
output, success, status = tm.execute_full()

# View results
print(f"Output: {output}")
print(f"Trace: {tm.get_execution_trace()}")
```

---

## Example: Parity Checker

**Purpose**: Check if the number of 1s in input is even (output 0) or odd (output 1)

**Definition**:
- **States**: q0 (even), q1 (odd), q2 (halt)
- **Input alphabet**: {0, 1}
- **Output alphabet**: {0, 1}

**Transitions**:
- `q0, 0 → q0, ε` (even+0 stays even)
- `q0, 1 → q1, ε` (even+1 becomes odd)
- `q1, 0 → q1, ε` (odd+0 stays odd)
- `q1, 1 → q0, ε` (odd+1 becomes even)
- `q0, # → q2, 0` (end with even result)
- `q1, # → q2, 1` (end with odd result)

**Example Execution**:
```
Input:  "11010"
Step 1: q0 + 1 → q1
Step 2: q1 + 1 → q0
Step 3: q0 + 0 → q0
Step 4: q0 + 1 → q1
Step 5: q1 + 0 → q1
Step 6: q1 + # → q2, Output: 1 (odd parity)
```

**Simulation Output**:
```
Step | State | Input | Output | Next State
-----|-------|-------|--------|------------
  1  |  q0   |   1   |   ε    |    q1
  2  |  q1   |   1   |   ε    |    q0
  3  |  q0   |   0   |   ε    |    q0
  4  |  q0   |   1   |   ε    |    q1
  5  |  q1   |   0   |   ε    |    q1
  6  |  q1   |   #   |   1    |    q2
```

---

## Example: Binary Incrementer

**Purpose**: Read a binary number and output the number + 1

**Definition**:
- **States**: q0 (reading input), q1 (adding 1), q2 (halt)
- **Input alphabet**: {0, 1}
- **Output alphabet**: {0, 1}

**Transitions**:
- `q0, 0 → q0, 0` (output 0s as-is)
- `q0, 1 → q0, 1` (output 1s as-is)
- `q0, # → q1, 1` (end of input, add 1)
- `q1, # → q2, #` (done)

**Example Execution**:
```
Input:  "11"
Step 1: q0 + 1 → q0, Output: 1
Step 2: q0 + 1 → q0, Output: 1
Step 3: q0 + # → q1, Output: 1 (this is +1)
Step 4: q1 + # → q2
Output: "111" (3 = 2 + 1)
```

---

## Turing Machine Simulation Details

### How the TM Simulates a Mealy Machine

1. **Tape contains**: The input string
2. **Head position**: Points to current input symbol
3. **State**: Mirrors the Mealy Machine state
4. **Transition**:
   - Read input symbol at head position
   - Look up transition in Mealy Machine
   - Update state
   - Append output to output buffer
   - Move head right

### Key Differences from Standard TM

- **Simplified**: No tape writing (read-only)
- **Purpose-specific**: Designed for FSM simulation
- **Output handling**: Accumulates in output buffer
- **Deterministic**: One transition per (state, input) pair

### Execution Flow

```
Initialize: tape = input, head = 0, state = q0, output = ""

repeat:
  symbol = tape[head]
  if (state, symbol) in transitions:
    next_state, out_symbol = transitions[state, symbol]
    state = next_state
    if out_symbol ≠ blank:
      output += out_symbol
    head += 1
  else:
    HALT
```

---

## Code Quality Features

✓ **Object-Oriented Design**: Clear class hierarchy
✓ **Type Hints**: Python type annotations throughout
✓ **Comprehensive Comments**: Theory of Computation explanations
✓ **Error Handling**: Validation and informative error messages
✓ **Modular Structure**: Separate concerns, reusable components
✓ **Documentation**: Inline and user-facing docs
✓ **Scalability**: Easy to add new machines and features

---

## Theory of Computation Concepts

### Finite Automata Hierarchy

```
          ┌─────────────────┐
          │  Turing Machine │
          │  (Decidable)    │
          └────────┬────────┘
                   │
          ┌────────▼────────┐
          │ Context-Free    │
          │ Grammar         │
          └────────┬────────┘
                   │
          ┌────────▼────────┐
          │ Mealy/Moore     │
          │ Machine (FSM)   │
          └────────┬────────┘
                   │
          ┌────────▼────────┐
          │    DFA/NFA      │
          │ (Regular Lang)  │
          └─────────────────┘
```

### Why This Matters

- **DFA**: Recognizes regular languages (pattern matching)
- **Mealy Machine**: DFA + output (translation)
- **Turing Machine**: Most powerful (algorithm simulation)
- This project shows: DFA concepts work within TM framework

### Church-Turing Thesis

> Any function that can be computed algorithmically can be computed by a Turing Machine

This simulator demonstrates that even finite state machines (simpler than algorithms) execute correctly on a TM.

---

## Requirements

- **Python**: 3.7+
- **Dependencies**: None required (Tkinter is included with Python)

Optional:
- `matplotlib`: For advanced visualizations
- `graphviz`: For state diagram generation

---

## Installation

```bash
# Clone or extract the project
cd "VI sem complex engineering problem"

# No installation needed - run directly
python cli_simulator.py       # CLI mode
python gui_simulator.py       # GUI mode
```

---

## Testing

Run the demo:
```bash
python cli_simulator.py
```

Or test specific examples:
```python
from tests.test_examples import run_all_tests
run_all_tests()
```

---

## Sample Output

### Parity Checker: Input "11010"

```
================================================================================
                        MEALY MACHINE TURING MACHINE SIMULATOR
================================================================================

Loading machine from: machines/parity_checker.json
✓ Machine loaded successfully

Input string: 11010
✓ Input validated

Running simulation...

============================================================
                    SIMULATION SUMMARY
============================================================
Input String:        11010
Output String:       1
Total Steps:         6
Final State:         q2
Tape Content:        11010
============================================================
EXECUTION TRACE
============================================================
Step | State | Input  | Output | Next State
-----|-------|--------|--------|----------
  1  |  q0   |   1    |   ε    |    q1
  2  |  q1   |   1    |   ε    |    q0
  3  |  q0   |   0    |   ε    |    q0
  4  |  q0   |   1    |   ε    |    q1
  5  |  q1   |   0    |   ε    |    q1
  6  |  q1   |   #    |   1    |    q2

✓ Simulation completed successfully
Status: Input exhausted
```

---

## Advanced Features

1. **Interactive Mode**: Step through execution manually
2. **Verbose Tracing**: Detailed tape and state information
3. **JSON Workflows**: Define machines externally
4. **GUI Interface**: No command-line knowledge required
5. **Scalability**: Add machines without code changes

---

## Educational Value

This project demonstrates:
✓ Finite State Machine concepts
✓ Turing Machine simulation
✓ State transition design
✓ Formal language processing
✓ Software architecture for automata
✓ GUI development
✓ File-based configuration

Suitable for:
- Undergraduate Theory of Computation course
- Complex Engineering Problem assignments
- Automata and Formal Languages studies
- Compiler design foundations

---

## Future Enhancements

- [ ] Non-deterministic Mealy Machine support
- [ ] State diagram visualization
- [ ] Multiple tape support
- [ ] Performance optimization for long inputs
- [ ] Export execution to various formats
- [ ] Custom alphabet symbols
- [ ] Machine minimization algorithms

---

## Author Notes

This project bridges the gap between abstract computational theory and practical implementation. By implementing FSM simulation on a Turing Machine, students gain deeper understanding of:

1. Why Turing Machines are universal
2. How different automata models relate
3. How to encode higher-level concepts in lower-level ones
4. Practical state machine implementation

The dual CLI/GUI approach allows use in educational settings (CLI for scripting) and professional settings (GUI for visualization).

---

## License

This project is provided for educational purposes.

---

## Theory of Computation References

1. **Sipser, M.** "Introduction to the Theory of Computation" (3rd ed.)
2. **Hopcroft, J. E.** "Introduction to Automata Theory, Languages, and Computation"
3. **Church, A.** "An Unsolvable Problem of Elementary Number Theory" (1936)
4. **Turing, A. M.** "On Computable Numbers..." (1937)

---

For questions or improvements, refer to the inline code documentation and Theory of Computation textbooks.
