# QUICKSTART Guide

## Installation (Under 1 minute!)

No additional installation needed! The project runs with Python 3.7+ standard library.

```bash
# Verify Python is installed
python --version    # Should show 3.7 or higher
```

## Running the Project

### Option 1: Graphical User Interface (Easiest!)

```bash
python gui_simulator.py
```

**What you'll see:**
1. Load Machine tab - Select preset machines or load from file
2. Simulate tab - Enter input and run simulation
3. Results tab - View execution traces and output
4. Help tab - Theory and usage documentation

### Option 2: Command-Line Interface (Fastest for testing!)

Run demo:
```bash
python cli_simulator.py
```

Simulate specific machine:
```bash
python cli_simulator.py machines/parity_checker.json "11010"
```

Verbose output:
```bash
python cli_simulator.py machines/parity_checker.json "11010" --verbose
```

Interactive mode (manual step-by-step):
```bash
python cli_simulator.py machines/parity_checker.json "11010" --interactive
```

### Option 3: Interactive Menu

```bash
python main.py
```

Select from menu: GUI, CLI, Demo, Tests, or Exit

### Option 4: Run Tests

```bash
python tests/test_examples.py
```

## Quick Examples

### Example 1: Parity Checker

Check if "11010" has even or odd number of 1s:

```bash
python cli_simulator.py machines/parity_checker.json "11010"
```

Expected output: **1** (odd parity - three 1s)

### Example 2: Binary Incrementer

Increment binary "11":

```bash
python cli_simulator.py machines/binary_incrementer.json "11"
```

Expected output: **111** (2 + 1 = 3 in binary)

### Example 3: Interactive Tutorial

```bash
python cli_simulator.py machines/parity_checker.json "101" --interactive
```

Press Enter to go through each step manually.

## Project Structure

```
.
├── src/                          # Core simulator code
│   ├── tape.py                  # Tape data structure
│   ├── mealy_machine.py         # Mealy Machine class
│   ├── turing_machine.py        # TM simulator
│   ├── config_loader.py         # JSON loading
│   └── visualizer.py            # Display utilities
├── machines/                     # Example machines
│   ├── parity_checker.json
│   ├── binary_incrementer.json
│   ├── binary_adder.json
│   └── even_checker.json
├── gui_simulator.py             # GUI application
├── cli_simulator.py             # CLI application
├── main.py                      # Interactive menu
├── README.md                    # Full documentation
└── tests/                       # Test suite
    └── test_examples.py
```

## Understanding the Output

### Trace Table Columns

| Column | Meaning |
|--------|---------|
| Step | Execution step number (1, 2, 3, ...) |
| State | Current state of the Mealy Machine |
| Input | Symbol read from the tape |
| Output | Symbol produced by this transition |
| Next State | State after this transition |

### Example: Binary "101" through Parity Checker

```
Step | State | Input | Output | Next State
-----|-------|-------|--------|------------
  1  |  q0   |   1   |   ε    |    q1      (odd)
  2  |  q1   |   0   |   ε    |    q1      (still odd)
  3  |  q1   |   1   |   ε    |    q0      (even again)
  4  |  q0   |   #   |   0    |    q2      (outputs 0 - even)
```

Final output: **0** (even parity - two 1s)

## Creating Custom Machines

### Step 1: Define your machine as JSON

```json
{
  "name": "My Machine",
  "states": ["q0", "q1"],
  "input_alphabet": ["0", "1"],
  "output_alphabet": ["a", "b"],
  "initial_state": "q0",
  "blank_symbol": "#",
  "transitions": [
    {
      "from": "q0",
      "input": "0",
      "to": "q1",
      "output": "a"
    }
  ]
}
```

### Step 2: Save to `machines/` directory

Save as `machines/my_machine.json`

### Step 3: Run simulation

```bash
python cli_simulator.py machines/my_machine.json "0"
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

**Solution**: Make sure you're running from the project root directory:
```bash
cd "VI sem complex engineering problem"
python cli_simulator.py
```

### "FileNotFoundError: machines/..."

**Solution**: Check that machine JSON files are in the `machines/` directory

### Invalid symbol in input

**Solution**: Use only symbols from the machine's input alphabet

Example: Parity Checker only accepts "0" and "1":
```bash
# This works:
python cli_simulator.py machines/parity_checker.json "10101"

# This fails (2 is not in alphabet):
python cli_simulator.py machines/parity_checker.json "102"
```

### GUI won't start

**Solution**: Tkinter must be installed with Python. On some Linux systems:
```bash
sudo apt-get install python3-tk    # Ubuntu/Debian
sudo dnf install python3-tkinter    # Fedora
```

## Key Concepts

**Mealy Machine**: A finite state machine where:
- Output depends on both state AND input
- Output is produced during transitions
- More expressive than Moore machines

**Turing Machine**: A theoretical computer with:
- Infinite tape (like computer memory)
- Read/write head (like CPU)
- State control (like instruction set)
- Can simulate any algorithm

**Why Simulate?**
This shows that FSMs (finite-state) can run on TMs (infinite-state), demonstrating
the hierarchy of computational models in Theory of Computation.

---

## Next Steps

1. **Try the examples**: Run each preset machine with different inputs
2. **Read the documentation**: Open `README.md` for detailed theory
3. **Explore the code**: Look at `src/` for clean, documented implementation
4. **Create custom machines**: Design your own FSM in JSON
5. **Study the trace**: Use verbose mode to understand step-by-step execution

## Learning Resources

- Introductory Theory: See `README.md` for concept overview
- In-code comments: Detailed Theory of Computation explanations
- GUI Help tab: Quick reference and examples
- Test suite: `tests/test_examples.py` shows various use cases

---

**Happy Simulating! 🎓**
