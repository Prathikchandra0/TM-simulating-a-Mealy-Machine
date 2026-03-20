"""
Command-line interface for Mealy Machine Turing Machine Simulator.

This module provides a console-based interface for running simulations
without requiring a GUI. It's useful for batch processing and testing.
"""

import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader, MachineConfigError
from src.visualizer import TraceVisualizer, InteractiveSimulator


def load_machine(machine_path: str) -> MealyMachine:
    """Load a machine from a JSON file."""
    try:
        return ConfigLoader.load_from_file(machine_path)
    except MachineConfigError as e:
        print(f"Error loading machine: {e}")
        sys.exit(1)


def validate_input(input_string: str, machine: MealyMachine) -> bool:
    """Validate that input string contains only symbols from input alphabet."""
    for symbol in input_string:
        if symbol not in machine.input_alphabet:
            print(f"Error: Symbol '{symbol}' not in input alphabet")
            print(f"Valid symbols: {sorted(machine.input_alphabet)}")
            return False
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mealy Machine Turing Machine Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_simulator.py machines/binary_incrementer.json "101"
  python cli_simulator.py machines/parity_checker.json "11010" --verbose
  python cli_simulator.py machines/parity_checker.json "10101" --interactive
        """
    )
    
    parser.add_argument(
        "machine",
        help="Path to machine configuration JSON file"
    )
    parser.add_argument(
        "input",
        help="Input string to process"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed execution trace"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive step-by-step mode"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("MEALY MACHINE TURING MACHINE SIMULATOR".center(80))
    print("=" * 80 + "\n")
    
    # Load machine
    print(f"Loading machine from: {args.machine}")
    machine = load_machine(args.machine)
    print("✓ Machine loaded successfully\n")
    
    # Validate input
    print(f"Input string: {args.input}")
    if not validate_input(args.input, machine):
        sys.exit(1)
    print("✓ Input validated\n")
    
    # Create TM
    tm = TuringMachine(machine)
    
    # Run simulation
    if args.interactive:
        print("Starting interactive simulation...\n")
        simulator = InteractiveSimulator(tm, args.input)
        simulator.run_interactive()
    else:
        print("Running simulation...\n")
        tm.initialize(args.input)
        output, success, status = tm.execute_full()
        
        # Display results
        TraceVisualizer.print_summary(tm, args.input)
        
        if args.verbose:
            TraceVisualizer.print_step_by_step(tm)
        else:
            TraceVisualizer.print_trace_table(tm, verbose=False)
        
        if success:
            print(f"\n✓ Simulation completed successfully")
        else:
            print(f"\n✗ Simulation did not complete")
        
        print(f"Status: {status}\n")


def demo():
    """Run a demo simulation."""
    print("\n" + "=" * 80)
    print("DEMO: Parity Checker".center(80))
    print("=" * 80 + "\n")
    
    machine = load_machine("machines/parity_checker.json")
    tm = TuringMachine(machine)
    
    # Show machine info
    machine.print_transition_table()
    
    # Run example
    print("\n" + "=" * 80)
    print("EXAMPLE: Input = '11010'")
    print("=" * 80)
    print("Expected: Output '1' (odd number of 1s)\n")
    
    tm.initialize("11010")
    output, success, status = tm.execute_full()
    
    TraceVisualizer.print_summary(tm, "11010")
    TraceVisualizer.print_trace_table(tm, verbose=True)
    
    # Another example
    print("\n" + "=" * 80)
    print("EXAMPLE: Input = '1100'")
    print("=" * 80)
    print("Expected: Output '0' (even number of 1s)\n")
    
    tm.reset()
    tm.initialize("1100")
    output, success, status = tm.execute_full()
    
    TraceVisualizer.print_summary(tm, "1100")
    TraceVisualizer.print_trace_table(tm, verbose=True)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - run demo
        demo()
    else:
        # Run with arguments
        main()
