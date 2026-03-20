# Complete Project Index & Guide

## Quick Navigation

### For First-Time Users
1. **Start Here**: [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start
2. **Learn by Examples**: Run `python getting_started.py`
3. **Try the GUI**: Run `python gui_simulator.py`
4. **Read Full Docs**: [README.md](README.md)

### For Educators/Researchers
1. **Theory Overview**: [README.md](README.md) - Theory of Computation section
2. **Technical Details**: [TECHNICAL.md](TECHNICAL.md)
3. **Code Examples**: See `src/` directory
4. **Test Suite**: Run `python tests/test_examples.py`

### For Advanced Users
1. **Source Code**: [src/](src/) directory
2. **Machine Definitions**: [machines/](machines/) directory  
3. **API Documentation**: Inline code docstrings
4. **Customization**: [TECHNICAL.md](TECHNICAL.md) - Extension Points

---

## File & Directory Guide

### Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| [README.md](README.md) | Comprehensive overview, theory, usage | 30 min |
| [QUICKSTART.md](QUICKSTART.md) | Fast startup guide | 5 min |
| [TECHNICAL.md](TECHNICAL.md) | Architecture, design, algorithms | 20 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete project summary | 10 min |
| [INDEX.md](INDEX.md) | This file - navigation guide | 5 min |

### Executable Scripts

| File | Purpose | How to Run |
|------|---------|-----------|
| [gui_simulator.py](gui_simulator.py) | Graphical interface | `python gui_simulator.py` |
| [cli_simulator.py](cli_simulator.py) | Command-line interface | `python cli_simulator.py [args]` |
| [getting_started.py](getting_started.py) | Interactive tutorial | `python getting_started.py` |
| [main.py](main.py) | Interactive menu | `python main.py` |

### Source Code Modules

#### Core Simulation ([src/](src/) directory)

| File | Class/Functions | Purpose |
|------|-----------------|---------|
| [tape.py](src/tape.py) | `Tape` | Turing Machine tape abstraction |
| [mealy_machine.py](src/mealy_machine.py) | `MealyMachine`, `MealyTransition` | FSM definition and transitions |
| [turing_machine.py](src/turing_machine.py) | `TuringMachine`, `TMTransitionType` | Simulation engine |
| [config_loader.py](src/config_loader.py) | `ConfigLoader`, `MachineConfigError` | JSON configuration management |
| [visualizer.py](src/visualizer.py) | `TraceVisualizer`, `InteractiveSimulator`, `TransitionTablePrinter` | Output formatting |
| [__init__.py](src/__init__.py) | Package info | Package initialization |

### Machine Definitions ([machines/](machines/) directory)

| File | Type | Purpose | Example Input | Expected Output |
|------|------|---------|----------------|-----------------|
| [parity_checker.json](machines/parity_checker.json) | FSM | Check odd/even 1s | "11010" | "1" (odd) |
| [binary_incrementer.json](machines/binary_incrementer.json) | FSM | Add 1 to binary | "11" | "111" |
| [binary_adder.json](machines/binary_adder.json) | FSM | Add two binary numbers | "10 11" | "101" |
| [even_checker.json](machines/even_checker.json) | FSM | Check if even | "1234" | "1" |

### Test Suite ([tests/](tests/) directory)

| File | Tests | Count | Status |
|------|-------|-------|--------|
| [test_examples.py](tests/test_examples.py) | Unit + Integration | 23 | ✓ All Pass |
| [__init__.py](tests/__init__.py) | Package info | - | - |

### Configuration Files

| File | Purpose |
|------|---------|
| [requirements.txt](requirements.txt) | Python dependencies (none required!) |
| [.git/](\.git/) | Version control (git repository) |

---

## How to Use Each Component

### 1. Command-Line Usage

#### Run GUI (Recommended for beginners)
```bash
python gui_simulator.py
```
**Best for**: Visual learners, interactive exploration

#### Run CLI with Demo
```bash
python cli_simulator.py
```
**Output**: Full demo of parity checker with examples

#### Simulate Specific Machine
```bash
python cli_simulator.py machines/parity_checker.json "11010" --verbose
```
**Best for**: Testing specific machines, scripting

#### Interactive Mode
```bash
python cli_simulator.py machines/parity_checker.json "101" --interactive
```
**Best for**: Step-by-step learning

#### Run Interactive Menu
```bash
python main.py
```
**Best for**: Choosing between different modes

### 2. Getting Started Script

```bash
python getting_started.py
```

Shows:
- Parity checker examples
- Binary incrementer examples
- Detailed execution traces
- Python API usage
- Error handling
- Machine comparison

### 3. Run Test Suite

```bash
python tests/test_examples.py
```

Results:
- 5 MealyMachine unit tests ✓
- 5 TuringMachine unit tests ✓
- 8 Parity checker functional tests ✓
- 5 Binary incrementer functional tests ✓
- **Total: 23/23 passing** ✓

### 4. Python API Usage

```python
from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader

# Load a machine
machine = ConfigLoader.load_from_file("machines/parity_checker.json")

# Create simulator
tm = TuringMachine(machine)

# Run simulation
tm.initialize("11010")
output, success, status = tm.execute_full()

# View results
print(f"Output: {output}")
print(f"Trace: {tm.execution_trace}")
```

---

## Common Tasks

### Task 1: Understand Parity Checker
```bash
# Visual exploration
python gui_simulator.py
# Select "Parity Checker" from presets
# Enter: "11010"
# View the execution trace

# Or read the documentation
# See: machines/parity_checker.json
# See: README.md - Example section
```

### Task 2: Create a Custom Machine
```bash
# 1. Create JSON file in machines/
# 2. Follow format from machines/parity_checker.json
# 3. Run: python cli_simulator.py machines/my_machine.json "input"
# 4. View results in execution trace
```

### Task 3: Run Automated Tests
```bash
python tests/test_examples.py
# See all 23 tests validate the implementation
```

### Task 4: Learn Theory
```bash
# Read: README.md (section "What is...")
# Read: TECHNICAL.md (section "Theoretical Foundations")
# Run: python getting_started.py (interactive examples)
```

### Task 5: Demonstrate to Others
```bash
# Show GUI
python gui_simulator.py

# Show CLI with interesting example
python cli_simulator.py machines/parity_checker.json "1110101" --verbose

# Run interactive demo
python getting_started.py
```

---

## File Relationships

```
getting_started.py
└── imports from:
    ├── src/mealy_machine.py
    ├── src/turing_machine.py
    ├── src/config_loader.py (loads machines/)
    └── src/visualizer.py

gui_simulator.py
└── imports from:
    ├── src/mealy_machine.py
    ├── src/turing_machine.py
    ├── src/config_loader.py (loads machines/)
    └── src/visualizer.py

cli_simulator.py
└── imports from:
    ├── src/mealy_machine.py
    ├── src/turing_machine.py
    ├── src/config_loader.py (loads machines/)
    └── src/visualizer.py

tests/test_examples.py
└── imports from:
    ├── src/mealy_machine.py
    ├── src/turing_machine.py
    └── src/config_loader.py (loads machines/)

src/turing_machine.py
└── imports from:
    ├── src/tape.py
    └── src/mealy_machine.py

src/config_loader.py
└── imports from:
    └── src/mealy_machine.py
```

---

## Example Scenarios

### Scenario 1: Academic Presentation
1. Run `python gui_simulator.py`
2. Load parity checker
3. Input: "11010"
4. Show execution trace
5. Explain each step
6. Discuss Turing Machine simulation
7. Ask audience to predict output for different inputs

### Scenario 2: Complete Learning Path
1. Read [QUICKSTART.md](QUICKSTART.md) (5 min)
2. Run `python getting_started.py` (10 min)
3. Try `python gui_simulator.py` (15 min)
4. Read [README.md](README.md) section by section (30 min)
5. Explore source code in [src/](src/) (20 min)
6. Read [TECHNICAL.md](TECHNICAL.md) (20 min)
7. Create custom machine and test (30 min)

### Scenario 3: Research/Extension
1. Read [TECHNICAL.md](TECHNICAL.md) thoroughly
2. Study source code for algorithms
3. Identify extension points
4. Implement new features
5. Test thoroughly
6. Document changes

---

## Quick Reference

### Common Commands

```bash
# GUI (easiest)
python gui_simulator.py

# Demo
python cli_simulator.py

# Specific test
python cli_simulator.py machines/parity_checker.json "101"

# Verbose trace
python cli_simulator.py machines/parity_checker.json "101" --verbose

# Interactive
python cli_simulator.py machines/parity_checker.json "101" --interactive

# Tutorial
python getting_started.py

# Tests
python tests/test_examples.py

# Menu
python main.py
```

### JSON Machine Template

```json
{
  "name": "Machine Name",
  "states": ["q0", "q1"],
  "input_alphabet": ["0", "1"],
  "output_alphabet": ["0", "1"],
  "initial_state": "q0",
  "blank_symbol": "#",
  "transitions": [
    {
      "from": "q0",
      "input": "0",
      "to": "q1",
      "output": "0"
    }
  ]
}
```

### Python Code Template

```python
from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader
from src.visualizer import TraceVisualizer

# Load machine
machine = ConfigLoader.load_from_file("machines/example.json")

# Or create manually
machine = MealyMachine(
    states={"q0", "q1"},
    input_alphabet={"a", "b"},
    output_alphabet={"x", "y"},
    initial_state="q0"
)
machine.add_transition("q0", "a", "q1", "x")

# Simulate
tm = TuringMachine(machine)
tm.initialize("aaa")
output, success, status = tm.execute_full()

# Visualize
tracer.print_trace_table(tm, verbose=True)
```

---

## Need Help?

### Error: "ModuleNotFoundError: No module named 'src'"
**Solution**: Make sure you're running from the project root directory
```bash
cd "VI sem complex engineering problem"
python cli_simulator.py
```

### Error: "FileNotFoundError: machines/..."
**Solution**: Check machine JSON files are in `machines/` directory

### Error: "Invalid symbol in input"
**Solution**: Use only symbols defined in machine's input alphabet

### How do I create a custom machine?
See: [machines/](machines/) - Copy an existing JSON file and modify it

### How do I understand the theory better?
See: [README.md](README.md) - "What is a Mealy Machine?" section
See: [TECHNICAL.md](TECHNICAL.md) - "Theoretical Foundations" section

### How do I extend the simulator?
See: [TECHNICAL.md](TECHNICAL.md) - "Extension Points" section

### Where's the source code?
See: [src/](src/) - All core modules with documentation

### How do I run tests?
```bash
python tests/test_examples.py
```

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Lines of Code | ~2,500 |
| Number of Classes | 8 |
| Number of Functions | 50+ |
| Test Coverage | 23 automated tests |
| Documentation Lines | 1,500+ |
| Machine Examples | 4 ready-to-use |
| External Dependencies | 0 (none required!) |

---

## Project Timeline

- **Planning**: Theory research, design
- **Implementation**: Core modules
- **Testing**: Comprehensive test suite
- **Documentation**: Multiple guides and examples
- **Polish**: Error handling, edge cases
- **Release**: Production ready

---

## Contact & Support

This is an educational project for Theory of Computation.

For questions, refer to:
1. Inline code comments (theory explanations)
2. [README.md](README.md) (comprehensive guide)
3. [TECHNICAL.md](TECHNICAL.md) (architecture)
4. Theory of Computation textbooks
5. Source code documentation strings

---

## License & Attribution

Created for educational purposes in Theory of Computation course.

---

**Project Status**: ✓ COMPLETE
**Version**: 1.0.0
**Last Updated**: March 2026

---

Start with [QUICKSTART.md](QUICKSTART.md) - you'll be running simulations in 5 minutes!
