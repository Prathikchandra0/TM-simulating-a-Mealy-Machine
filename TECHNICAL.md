# Technical Documentation

## Architecture Overview

### System Design Pattern

The simulator uses a **modular, layered architecture**:

```
┌─────────────────────────────────────┐
│   User Interface Layer              │
│  ├─ GUI (Tkinter)                  │
│  └─ CLI (argparse)                 │
├─────────────────────────────────────┤
│   Visualization Layer               │
│  ├─ TraceVisualizer                │
│  └─ InteractiveSimulator            │
├─────────────────────────────────────┤
│   Configuration Layer               │
│  └─ ConfigLoader (JSON)             │
├─────────────────────────────────────┤
│   Core Simulation Layer             │
│  ├─ TuringMachine (Simulator)       │
│  └─ MealyMachine (Definition)       │
├─────────────────────────────────────┤
│   Data Structure Layer              │
│  └─ Tape (Storage)                  │
└─────────────────────────────────────┘
```

## Core Components Detailed

### 1. Tape (src/tape.py)

**Purpose**: Simulates the infinite tape of a Turing Machine

**Implementation**:
```python
class Tape:
    tape: List[str]          # Dynamic list of cells
    head_position: int       # Current position
    blank_symbol: str = "#"  # End-of-input marker
```

**Key Operations** (O(1) amortized):
- `read()`: Get symbol at head position
- `write(symbol)`: Write to current position
- `move(direction)`: Update head position
- `reset()`: Clear tape and reset head

**Memory Management**:
- Tape grows dynamically as needed
- Left expansion: Insert and shift
- Right expansion: Append
- Maximum size: Adaptively sized for input

### 2. MealyMachine (src/mealy_machine.py)

**Purpose**: Defines the finite state machine to be simulated

**Data Structure**:
```python
class MealyMachine:
    states: Set[str]                              # Q
    input_alphabet: Set[str]                      # Σ
    output_alphabet: Set[str]                     # Δ
    initial_state: str                            # q0
    transitions: Dict[Tuple[str, str],           # δ function
                      Tuple[str, str]]
    blank_symbol: str                             # ε
```

**Transition Function**:
```
δ: Q × (Σ ∪ {ε}) → Q × (Δ ∪ {ε})
δ(state, input) = (next_state, output)
```

**Validation**:
- States are validated against defined set
- Symbols checked against alphabets
- No undefined transitions allowed
- Initial state must be in states set

**Example**: Parity Checker
```
States: {q0 (even), q1 (odd), q2 (halt)}
Σ: {0, 1}, Δ: {0, 1}
δ(q0, 1) = (q1, ε)    # even + 1 → odd
δ(q1, 1) = (q0, ε)    # odd + 1 → even
δ(q0, #) = (q2, 0)    # end in even state → output 0
δ(q1, #) = (q2, 1)    # end in odd state → output 1
```

### 3. TuringMachine (src/turing_machine.py)

**Purpose**: Simulates the Mealy Machine using TM approach

**Execution Algorithm**:

```python
def execute_full(input_string, max_steps=10000):
    """Main simulation loop"""
    tape.initialize(input_string)
    current_state = initial_state
    output_buffer = ""
    
    for step in range(max_steps):
        # Step 1: Read
        symbol = tape.read()
        
        # Step 2: Lookup
        if (current_state, symbol) not in transitions:
            return output_buffer, True, "Halted"
        
        next_state, output = transitions[current_state, symbol]
        
        # Step 3: Update
        current_state = next_state
        if output != blank:
            output_buffer += output
        
        # Step 4: Move
        tape.move('R')
        
        # Step 5: Check halt condition
        if tape.head_position > len(tape.tape):
            return output_buffer, True, "Input exhausted"
    
    return output_buffer, False, "Max steps exceeded"
```

**Execution Trace**:

Each step recorded as:
```python
trace_entry = {
    'step': int,
    'state': str,
    'input': str,
    'next_state': str,
    'output': str,
    'tape': str,
    'head_pos': int
}
```

**Time Complexity**:
- **Per step**: O(1) - constant time operations
- **Full execution**: O(n) where n is input length
- **Space complexity**: O(n) for tape storage

### 4. ConfigLoader (src/config_loader.py)

**JSON Schema**:

```json
{
  "name": "string",
  "description": "string",
  "states": ["string"],
  "input_alphabet": ["string"],
  "output_alphabet": ["string"],
  "initial_state": "string",
  "blank_symbol": "string",
  "transitions": [
    {
      "from": "string",
      "input": "string",
      "to": "string",
      "output": "string"
    }
  ]
}
```

**Validation Steps**:

1. JSON parsing
2. Required field check
3. State validation
4. Alphabet validation
5. Transition validation
6. Consistency check

**Error Handling**:

```python
class MachineConfigError(Exception):
    """Configuration-related errors"""
    pass
```

### 5. Visualizer (src/visualizer.py)

**Components**:

1. **TraceVisualizer**: Formats execution trace
   - Print trace table
   - Print summary
   - Print step-by-step details

2. **TransitionTablePrinter**: Various table formats
   - Mealy table
   - State-output mappings

3. **InteractiveSimulator**: Manual step control
   - Next step
   - Skip to end
   - Quit

## Theoretical Foundations

### Mealy Machine Formalism

A Mealy machine is 6-tuple: M = (Q, Σ, Δ, δ, λ, q0)

Where:
- **Q**: Finite set of states
- **Σ**: Input alphabet
- **Δ**: Output alphabet
- **δ: Q × Σ → Q**: State transition function
- **λ: Q × Σ → Δ**: Output function
- **q0 ∈ Q**: Initial state

Combined: δ: Q × Σ → Q × Δ

### Why Turing Machines Can Simulate Mealy Machines

**Lemma**: Any Mealy Machine can be simulated by a Turing Machine.

**Proof sketch**:
1. TM has infinite tape ⊇ finite FSM alphabet
2. TM state space includes FSM states
3. TM read operation ≥ FSM input reading
4. TM write operation ≥ FSM output generation
5. TM move right ≥ linear input processing

**Conclusion**: FSM ⊆ TM in terms of computational capability

### Input/Output Processing

**Input Processing**:
- Raw string → Tape cells
- Each character at position i
- Head starts at position 0
- Blank symbol (#) marks end

**Output Generation**:
- Non-blank output symbols accumulated
- Stored in output buffer
- Final string assembled after execution

**Example**:
```
Input:  "101"
Tape:   [1][0][1][#]...(blanks)
        ^0  1  2  3

Processing:
- Read tape[0]='1' → output 'x' → move right
- Read tape[1]='0' → output 'y' → move right
- Read tape[2]='1' → output 'z' → move right
- Read tape[3]='#' → halt

Output: "xyz"
```

## Performance Characteristics

### Space Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| Tape | O(n) | Linear with input length |
| States | O(s) | s = number of states |
| Transitions | O(s×a) | s×a = state-input pairs |
| Execution trace | O(n) | One record per step |
| Output buffer | O(m) | m = output length |

**Total**: O(n + s + a) dominated by input length

### Time Complexity

| Operation | Complexity |
|-----------|-----------|
| Tape read/write | O(1) |
| Transition lookup | O(1) amortized |
| Single step | O(1) |
| Full execution | O(n) |

### Scalability

- **Input size**: Tested up to 10,000 characters
- **State count**: No practical limit (Python memory)
- **Alphabet size**: Limited by memory
- **Transitions**: O(1) lookup using hash map

## Implementation Design Decisions

### 1. Dynamic Tape vs Array

**Choice**: Dynamic list (Python list)
**Rationale**:
- Easy expansion
- Automatic memory management
- O(1) amortized append
- Simple implementation

### 2. Transition Storage

**Choice**: Dictionary (hash map)
```python
transitions: Dict[Tuple[str, str], Tuple[str, str]]
```

**Rationale**:
- O(1) average lookup
- Sparse representation (only defined transitions)
- Easy to iterate

### 3. Execution Trace

**Choice**: List of dictionaries
**Rationale**:
- Complete history preservation
- Easy visualization
- Debugging support
- JSON-serializable

### 4. Blank Symbol Representation

**Choice**: Special symbol '#'
**Rationale**:
- Distinct from normal inputs
- Standard in automata theory
- Configurable per machine

## Error Handling Strategy

### Validation Layers

1. **Configuration validation** (Loading)
   - File format check
   - Schema validation
   - State consistency

2. **Runtime validation** (Execution)
   - Input alphabet check
   - Transition existence
   - Tape bounds

3. **User input validation** (UI)
   - Non-empty input
   - Alphabet membership
   - Machine selection

### Exception Types

```python
class MachineConfigError(Exception):
    """Configuration-related errors"""
    pass

# Implicit exceptions:
# - ValueError: Invalid state/symbol
# - FileNotFoundError: Missing config file
# - KeyError: Missing transitions
```

## Testing Strategy

### Test Categories

1. **Unit Tests** (Core classes)
   - MealyMachine creation
   - Transition management
   - TM initialization

2. **Functional Tests** (Algorithm correctness)
   - Parity checker
   - Binary incrementer
   - Edge cases

3. **Integration Tests** (Everything together)
   - Config loading
   - Full simulation
   - Output correctness

### Test Coverage

```
src/tape.py              ✓ Covered
src/mealy_machine.py     ✓ Covered
src/turing_machine.py    ✓ Covered
src/config_loader.py     ✓ Covered
src/visualizer.py        ✓ Covered (manual)
```

Run tests:
```bash
python tests/test_examples.py
```

## Extension Points

### Adding New Machines

1. Define JSON file in `machines/`
2. Load with `ConfigLoader.load_from_file()`
3. Create TM simulator
4. Run execution

### Custom Visualizations

```python
from src.visualizer import TraceVisualizer

class CustomVisualizer(TraceVisualizer):
    def custom_format(self, tm):
        # Your visualization logic
        pass
```

### Enhanced Features

- State diagram generation (graphviz)
- Performance profiling
- Animated simulation
- Machine minimization
- NFA support

## Dependencies

### Standard Library Only

- `typing`: Type hints
- `enum`: Enumeration
- `dataclass`: Data structures
- `json`: Configuration
- `tkinter`: GUI
- `argparse`: CLI

### No External Dependencies Required

This is intentional for:
- Easy deployment
- Harvard/academic computers
- Offline usage
- Installation simplicity

## Code Quality Metrics

### Conventions Used

- **PEP 8**: Style guide
- **Type hints**: Full coverage
- **Docstrings**: Google style
- **Comments**: Explain theory

### Complexity Analysis

- **Cyclomatic complexity**: Low (simple state machine)
- **Function size**: Small (< 50 lines typical)
- **Class cohesion**: High (single responsibility)
- **Coupling**: Low (layer-based)

## Future Optimization Opportunities

1. **Lazy tape initialization**: Don't allocate full array upfront
2. **Caching**: Pre-compute transition results
3. **Parallel simulation**: Multiple inputs
4. **Compiled backends**: Python → cython → C
5. **GPU acceleration**: For large alphabets

---

This documentation provides the complete technical foundation for understanding,
maintaining, and extending the simulator.
