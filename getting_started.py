#!/usr/bin/env python3
"""
GETTING_STARTED.py - Run this file to see interactive examples!

This script demonstrates all key features of the Mealy Machine Turing Machine Simulator.
It's the quickest way to understand how everything works!

Just run:
    python getting_started.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader
from src.visualizer import TraceVisualizer


def print_section(title):
    """Print a section header."""
    print("\n" + "="*80)
    print(f"  {title}".ljust(80))
    print("="*80)


def example_1_parity_checker():
    """Example 1: Parity Checker Machine"""
    print_section("EXAMPLE 1: PARITY CHECKER")
    print("""
A Parity Checker determines if the number of 1s in a binary string is:
- Even (output 0)
- Odd (output 1)

This is implemented as a Mealy Machine with:
- States: q0 (tracking even count), q1 (tracking odd count), q2 (halt)
- Input: Binary digits 0 and 1
- Output: 0 for even, 1 for odd
""")
    
    machine = ConfigLoader.load_from_file("machines/parity_checker.json")
    tm = TuringMachine(machine)
    
    test_cases = ["0", "1", "11", "101", "11010"]
    
    print("Running parity checker on various inputs:\n")
    
    for input_str in test_cases:
        tm.reset()
        tm.initialize(input_str)
        output, success, status = tm.execute_full()
        
        # Count 1s in input
        count_ones = input_str.count('1')
        parity = "even" if count_ones % 2 == 0 else "odd"
        
        print(f"  Input: '{input_str}' ({count_ones} ones = {parity})")
        print(f"    → Output: '{output}' (correct: {output == str(count_ones % 2)})")
        print(f"    → Steps: {len(tm.execution_trace)}")


def example_2_binary_incrementer():
    """Example 2: Binary Incrementer Machine"""
    print_section("EXAMPLE 2: BINARY INCREMENTER")
    print("""
A Binary Incrementer reads a binary number and outputs the number + 1.

This is implemented as a Mealy Machine with:
- States: q0 (reading), q1 (adding 1), q2 (halt)
- Input: Binary digits 0 and 1
- Output: The binary representation of input + 1
""")
    
    machine = ConfigLoader.load_from_file("machines/binary_incrementer.json")
    tm = TuringMachine(machine)
    
    test_cases = ["0", "1", "10", "11", "100", "111"]
    
    print("Running binary incrementer on various inputs:\n")
    
    for input_str in test_cases:
        tm.reset()
        tm.initialize(input_str)
        output, success, status = tm.execute_full()
        
        # Convert to decimal for verification
        input_decimal = int(input_str, 2) if input_str else 0
        output_decimal = int(output, 2) if output else 0
        
        print(f"  Input: '{input_str}' (decimal: {input_decimal})")
        print(f"    → Output: '{output}' (decimal: {output_decimal})")
        print(f"    → Correct: {output_decimal == input_decimal + 1}")
        print(f"    → Steps: {len(tm.execution_trace)}")


def example_3_detailed_trace():
    """Example 3: Detailed Execution Trace"""
    print_section("EXAMPLE 3: DETAILED EXECUTION TRACE")
    print("""
Let's see exactly what happens step-by-step when we process an input.
Watch how the machine's state changes, reads input, and generates output.
""")
    
    machine = ConfigLoader.load_from_file("machines/parity_checker.json")
    tm = TuringMachine(machine)
    
    input_str = "101"
    tm.initialize(input_str)
    tm.execute_full()
    
    print(f"\nInput: '{input_str}'")
    print("\nStep-by-Step Trace:\n")
    
    trace = tm.execution_trace
    for entry in trace:
        print(f"Step {entry['step']}:")
        print(f"  Current State:  {entry['state']}")
        print(f"  Reading:        '{entry['input']}'")
        print(f"  Output:         '{entry['output']}' ({('(nothing)' if entry['output'] == '#' else '(produced)')}")
        print(f"  Next State:     {entry['next_state']}")
        print()
    
    print(f"Final Output: '{tm.output_buffer}'")
    print(f"Final State: {tm.current_state}")


def example_4_api_usage():
    """Example 4: Using the Python API Directly"""
    print_section("EXAMPLE 4: PYTHON API USAGE")
    print("""
You can use the simulator directly in Python code to:
- Define custom machines
- Run simulations
- Process results programmatically
""")
    
    # Create a simple machine: echo machine that outputs what it reads
    print("Creating a custom Echo Machine...")
    
    machine = MealyMachine(
        states={"q0", "q1"},
        input_alphabet={"a", "b"},
        output_alphabet={"a", "b"},
        initial_state="q0"
    )
    
    # Add transitions: echo the input
    machine.add_transition("q0", "a", "q0", "a")
    machine.add_transition("q0", "b", "q0", "b")
    machine.add_transition("q0", "#", "q1", "#")
    
    tm = TuringMachine(machine)
    
    # Run simulation
    input_str = "aba"
    tm.initialize(input_str)
    output, success, status = tm.execute_full()
    
    print(f"\nEcho Machine Test:")
    print(f"  Input:  '{input_str}'")
    print(f"  Output: '{output}'")
    print(f"  Success: {success}")
    print(f"  Status: {status}")


def example_5_error_handling():
    """Example 5: Error Handling"""
    print_section("EXAMPLE 5: ERROR HANDLING & VALIDATION")
    print("""
The simulator validates inputs and handles errors gracefully.
""")
    
    machine = ConfigLoader.load_from_file("machines/parity_checker.json")
    tm = TuringMachine(machine)
    
    print("Test 1: Valid input")
    print("  Input: '101' (valid binary)")
    tm.initialize("101")
    output, success, status = tm.execute_full()
    print(f"  Result: ✓ Success - Output: '{output}'")
    
    print("\nTest 2: Invalid input")
    print("  Input: '102' (contains invalid symbol '2')")
    try:
        tm.initialize("102")
        output, success, status = tm.execute_full()
        if not success:
            print(f"  Result: ✗ Caught - {status}")
    except Exception as e:
        print(f"  Result: ✗ Caught - {e}")
    
    print("\nTest 3: Empty input")
    print("  Input: '' (empty string)")
    tm.initialize("")
    output, success, status = tm.execute_full()
    print(f"  Result: Handled - Output: '{output}', Status: {status}")


def example_6_comparison():
    """Example 6: Comparing Machine Outputs"""
    print_section("EXAMPLE 6: COMPARING DIFFERENT MACHINES")
    print("""
Different machines process the same input differently.
Let's compare parity checker and binary incrementer on "11":
""")
    
    parity_machine = ConfigLoader.load_from_file("machines/parity_checker.json")
    incr_machine = ConfigLoader.load_from_file("machines/binary_incrementer.json")
    
    input_str = "11"
    
    print(f"\nInput: '{input_str}'\n")
    
    # Parity checker
    tm1 = TuringMachine(parity_machine)
    tm1.initialize(input_str)
    output1, _, _ = tm1.execute_full()
    print(f"Parity Checker:")
    print(f"  Output:    '{output1}'")
    print(f"  Meaning:   0=even parity, 1=odd parity)")
    print(f"  Analysis:  Two 1s → even parity → output 0)")
    print(f"  Steps:     {len(tm1.execution_trace)}")
    
    # Binary incrementer
    tm2 = TuringMachine(incr_machine)
    tm2.initialize(input_str)
    output2, _, _ = tm2.execute_full()
    print(f"\nBinary Incrementer:")
    print(f"  Output:    '{output2}'")
    print(f"  Meaning:   Binary representation")
    print(f"  Analysis:  11 (binary)=3 → 3+1=4 → 100 (binary)")
    print(f"  Steps:     {len(tm2.execution_trace)}")
    
    print(f"\nConclusion: Same input, different machines → different outputs!")


def main():
    """Run all examples."""
    print("\n" + "#"*80)
    print("# MEALY MACHINE TURING MACHINE SIMULATOR - GETTING STARTED".ljust(79) + "#")
    print("#"*80)
    
    print("""
This script demonstrates the key features and capabilities of the simulator.

We'll show:
1. Parity Checker - Binary digit analysis
2. Binary Incrementer - Arithmetic operation
3. Detailed Trace - Step-by-step execution
4. Python API - Programmatic usage
5. Error Handling - Validation and error recovery
6. Machine Comparison - Different machines on same input
""")
    
    try:
        example_1_parity_checker()
        example_2_binary_incrementer()
        example_3_detailed_trace()
        example_4_api_usage()
        example_5_error_handling()
        example_6_comparison()
        
        # Final summary
        print_section("WHAT YOU'VE LEARNED")
        print("""
✓ Mealy Machines: FSM with output generation
✓ TM Simulation: How to run FSM on Turing Machine
✓ Execution Trace: Step-by-step computation tracking
✓ API Usage: Programmatic machine creation and simulation
✓ Error Handling: Robust input validation
✓ Machine Variety: Different machines for different tasks

NEXT STEPS:
1. Run the GUI: python gui_simulator.py
2. Try the CLI: python cli_simulator.py machines/parity_checker.json "11010"
3. Create a machine: Add JSON file to machines/
4. Run tests: python tests/test_examples.py
5. Read docs: Check README.md for detailed documentation

Happy exploring!
""")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you're running this from the project directory!")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
