#!/usr/bin/env python3
"""
Final verification script for the Mealy Machine TM Simulator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def main():
    print('='*70)
    print('FINAL VERIFICATION'.center(70))
    print('='*70)

    # Test 1: Import all modules
    print('\n[1/5] Testing module imports...')
    try:
        from src.tape import Tape
        from src.mealy_machine import MealyMachine
        from src.turing_machine import TuringMachine
        from src.config_loader import ConfigLoader
        from src.visualizer import TraceVisualizer
        print('  ✓ All modules import successfully')
    except Exception as e:
        print(f'  ✗ Import failed: {e}')
        return False

    # Test 2: Load a machine
    print('\n[2/5] Testing machine loading...')
    try:
        machine = ConfigLoader.load_from_file('machines/parity_checker.json')
        print(f'  ✓ Loaded parity checker ({len(machine.transitions)} transitions)')
    except Exception as e:
        print(f'  ✗ Load failed: {e}')
        return False

    # Test 3: Run simulation
    print('\n[3/5] Testing simulation execution...')
    try:
        tm = TuringMachine(machine)
        tm.initialize('11010')
        output, success, status = tm.execute_full()
        print(f'  ✓ Simulation completed: input="11010" → output="{output}" (expected: "1")')
        if output != '1':
            print(f'  ✗ Wrong output! Expected "1", got "{output}"')
            return False
    except Exception as e:
        print(f'  ✗ Simulation failed: {e}')
        return False

    # Test 4: Test API usage
    print('\n[4/5] Testing Python API...')
    try:
        m = MealyMachine(
            states={'q0', 'q1'},
            input_alphabet={'0', '1'},
            output_alphabet={'a', 'b'},
            initial_state='q0'
        )
        m.add_transition('q0', '0', 'q1', 'a')
        m.add_transition('q1', '1', 'q0', 'b')
        m.add_transition('q0', '#', 'q0', '#')
        
        tm2 = TuringMachine(m)
        tm2.initialize('01')
        print(f'  ✓ Custom machine created and simulated')
    except Exception as e:
        print(f'  ✗ API test failed: {e}')
        return False

    # Test 5: Run subset of tests
    print('\n[5/5] Testing test suite...')
    try:
        from tests.test_examples import TestParity
        
        p1, f1 = TestParity.run()
        
        if f1 == 0:
            print(f'  ✓ Parity tests passed: {p1}/{p1} tests')
        else:
            print(f'  ✗ {f1} tests failed!')
            return False
    except Exception as e:
        print(f'  ✗ Test suite failed: {e}')
        return False

    print('\n' + '='*70)
    print('ALL VERIFICATIONS PASSED ✓'.center(70))
    print('='*70)
    print('\nProject is complete and ready for use!')
    print('\nQuick Start:')
    print('  - GUI:      python gui_simulator.py')
    print('  - CLI:      python cli_simulator.py')
    print('  - Tutorial: python getting_started.py')
    print('  - Docs:     Read README.md')
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
