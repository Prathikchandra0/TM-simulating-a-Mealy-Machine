#!/usr/bin/env python3
"""
Main entry point for Mealy Machine Turing Machine Simulator.

This script provides a menu to choose between:
- Running the GUI
- Running the CLI
- Running tests
- Running a demo
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def display_menu():
    """Display the main menu."""
    print("\n" + "="*80)
    print("MEALY MACHINE TURING MACHINE SIMULATOR".center(80))
    print("="*80)
    print("\nMain Menu:")
    print("  1. Launch GUI Interface")
    print("  2. Run Command-Line Interface")
    print("  3. Run Demo Simulation")
    print("  4. Run Test Suite")
    print("  5. Exit")
    print("\n" + "-"*80)
    
    choice = input("Enter your choice (1-5): ").strip()
    return choice


def main():
    """Main entry point."""
    while True:
        choice = display_menu()
        
        if choice == "1":
            print("\nLaunching GUI Interface...")
            try:
                from gui_simulator import main as gui_main
                gui_main()
            except ImportError as e:
                print(f"Error: Could not import GUI module: {e}")
                print("Make sure you're running from the project root directory.")
        
        elif choice == "2":
            print("\nLaunching Command-Line Interface...")
            print("Usage: python cli_simulator.py <machine.json> <input_string> [options]")
            print("Run: python cli_simulator.py --help for more information")
            try:
                from cli_simulator import demo
                demo()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            print("\nRunning Demo Simulation...")
            try:
                from cli_simulator import demo
                demo()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            print("\nRunning Test Suite...")
            try:
                from tests.test_examples import run_all_tests
                run_all_tests()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("\nExiting. Thank you for using the simulator!")
            sys.exit(0)
        
        else:
            print(f"\nInvalid choice '{choice}'. Please enter a number 1-5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
