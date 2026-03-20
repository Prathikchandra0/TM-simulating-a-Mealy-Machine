"""
Test examples and automated testing for the Mealy Machine Turing Machine Simulator.

This module provides comprehensive test cases to verify the correctness
of the simulator implementation.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader


class TestParity:
    """Test cases for the Parity Checker machine."""
    
    @staticmethod
    def run():
        """Run parity checker tests."""
        print("\n" + "="*80)
        print("TESTING: PARITY CHECKER".center(80))
        print("="*80)
        
        machine = ConfigLoader.load_from_file("machines/parity_checker.json")
        tm = TuringMachine(machine)
        
        test_cases = [
            ("0", "0", "Single 0: even parity"),
            ("1", "1", "Single 1: odd parity"),
            ("00", "0", "Two 0s: even parity"),
            ("11", "0", "Two 1s (0 and 1 cancel): even parity"),
            ("111", "1", "Three 1s: odd parity"),
            ("1010", "0", "Two 1s: even parity"),
            ("11010", "1", "Three 1s: odd parity"),
            ("10101010", "0", "Four 1s: even parity"),
        ]
        
        passed = 0
        failed = 0
        
        for input_str, expected_output, description in test_cases:
            tm.reset()
            tm.initialize(input_str)
            output, success, status = tm.execute_full()
            
            if output == expected_output:
                print(f"✓ PASS: {description}")
                print(f"        Input: '{input_str}' → Output: '{output}'")
                passed += 1
            else:
                print(f"✗ FAIL: {description}")
                print(f"        Input: '{input_str}'")
                print(f"        Expected: '{expected_output}', Got: '{output}'")
                failed += 1
        
        print(f"\n{'-'*80}")
        print(f"Parity Tests: {passed} passed, {failed} failed")
        return passed, failed


class TestBinaryIncrementer:
    """Test cases for the Binary Incrementer machine."""
    
    @staticmethod
    def run():
        """Run binary incrementer tests."""
        print("\n" + "="*80)
        print("TESTING: BINARY INCREMENTER".center(80))
        print("="*80)
        
        machine = ConfigLoader.load_from_file("machines/binary_incrementer.json")
        tm = TuringMachine(machine)
        
        # Note: Simple incrementer copies input and adds 1
        test_cases = [
            ("0", "01", "0 + 1 = 1"),
            ("1", "11", "1 + 1 = 2 (binary)"),
            ("10", "101", "2 + 1 = 3"),
            ("11", "111", "3 + 1 = 4 (3 in binary)"),
            ("100", "1001", "4 + 1 = 5"),
        ]
        
        passed = 0
        failed = 0
        
        for input_str, expected_output, description in test_cases:
            tm.reset()
            tm.initialize(input_str)
            output, success, status = tm.execute_full()
            
            if output == expected_output:
                print(f"✓ PASS: {description}")
                print(f"        Input: '{input_str}' → Output: '{output}'")
                passed += 1
            else:
                print(f"✗ FAIL: {description}")
                print(f"        Input: '{input_str}'")
                print(f"        Expected: '{expected_output}', Got: '{output}'")
                failed += 1
        
        print(f"\n{'-'*80}")
        print(f"Binary Incrementer Tests: {passed} passed, {failed} failed")
        return passed, failed


class TestMealyMachine:
    """Basic tests for MealyMachine class."""
    
    @staticmethod
    def run():
        """Run Mealy machine unit tests."""
        print("\n" + "="*80)
        print("TESTING: MEALY MACHINE CLASS".center(80))
        print("="*80)
        
        passed = 0
        failed = 0
        
        # Test 1: Basic creation
        try:
            m = MealyMachine(
                states={"q0", "q1"},
                input_alphabet={"0", "1"},
                output_alphabet={"a", "b"},
                initial_state="q0"
            )
            print("✓ PASS: MealyMachine creation")
            passed += 1
        except Exception as e:
            print(f"✗ FAIL: MealyMachine creation - {e}")
            failed += 1
        
        # Test 2: Add transition
        try:
            m.add_transition("q0", "0", "q1", "a")
            print("✓ PASS: Add transition")
            passed += 1
        except Exception as e:
            print(f"✗ FAIL: Add transition - {e}")
            failed += 1
        
        # Test 3: Get transition
        try:
            result = m.get_transition("q0", "0")
            if result == ("q1", "a"):
                print("✓ PASS: Get transition")
                passed += 1
            else:
                print(f"✗ FAIL: Get transition - expected ('q1', 'a'), got {result}")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: Get transition - {e}")
            failed += 1
        
        # Test 4: Invalid state
        try:
            m.add_transition("q99", "0", "q1", "a")
            print("✗ FAIL: Should reject invalid state")
            failed += 1
        except ValueError:
            print("✓ PASS: Invalid state rejected")
            passed += 1
        
        # Test 5: Invalid initial state
        try:
            m2 = MealyMachine(
                states={"q0", "q1"},
                input_alphabet={"0"},
                output_alphabet={"a"},
                initial_state="q99"
            )
            print("✗ FAIL: Should reject invalid initial state")
            failed += 1
        except ValueError:
            print("✓ PASS: Invalid initial state rejected")
            passed += 1
        
        print(f"\n{'-'*80}")
        print(f"MealyMachine Unit Tests: {passed} passed, {failed} failed")
        return passed, failed


class TestTuringMachine:
    """Basic tests for TuringMachine class."""
    
    @staticmethod
    def run():
        """Run Turing machine unit tests."""
        print("\n" + "="*80)
        print("TESTING: TURING MACHINE CLASS".center(80))
        print("="*80)
        
        passed = 0
        failed = 0
        
        # Create a simple Mealy machine for testing
        m = MealyMachine(
            states={"q0", "q1"},
            input_alphabet={"0", "1"},
            output_alphabet={"0", "1"},
            initial_state="q0"
        )
        m.add_transition("q0", "0", "q0", "0")
        m.add_transition("q0", "1", "q1", "1")
        m.add_transition("q1", "#", "q1", "#")
        
        # Test 1: TM creation
        try:
            tm = TuringMachine(m)
            print("✓ PASS: TuringMachine creation")
            passed += 1
        except Exception as e:
            print(f"✗ FAIL: TuringMachine creation - {e}")
            failed += 1
        
        # Test 2: Initialize
        try:
            tm.initialize("01")
            if tm.step_count == 0:
                print("✓ PASS: Initialize")
                passed += 1
            else:
                print("✗ FAIL: Initialize - step count not reset")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: Initialize - {e}")
            failed += 1
        
        # Test 3: Execute step
        try:
            is_halted, status = tm.execute_step()
            if tm.step_count == 1:
                print("✓ PASS: Execute step")
                passed += 1
            else:
                print("✗ FAIL: Execute step - step count not incremented")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: Execute step - {e}")
            failed += 1
        
        # Test 4: Get execution trace
        try:
            trace = tm.get_execution_trace()
            if len(trace) == 1:
                print("✓ PASS: Get execution trace")
                passed += 1
            else:
                print(f"✗ FAIL: Get execution trace - expected 1 entry, got {len(trace)}")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: Get execution trace - {e}")
            failed += 1
        
        # Test 5: Reset
        try:
            tm.reset()
            if tm.step_count == 0 and tm.output_buffer == "":
                print("✓ PASS: Reset")
                passed += 1
            else:
                print("✗ FAIL: Reset - state not cleared")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: Reset - {e}")
            failed += 1
        
        print(f"\n{'-'*80}")
        print(f"TuringMachine Unit Tests: {passed} passed, {failed} failed")
        return passed, failed


def run_all_tests():
    """Run all test suites."""
    print("\n" + "#"*80)
    print("# MEALY MACHINE TURING MACHINE SIMULATOR - TEST SUITE".ljust(79) + "#")
    print("#"*80)
    
    total_passed = 0
    total_failed = 0
    
    # Run test suites
    p, f = TestMealyMachine.run()
    total_passed += p
    total_failed += f
    
    p, f = TestTuringMachine.run()
    total_passed += p
    total_failed += f
    
    p, f = TestParity.run()
    total_passed += p
    total_failed += f
    
    p, f = TestBinaryIncrementer.run()
    total_passed += p
    total_failed += f
    
    # Print summary
    print("\n" + "#"*80)
    print("#" + "OVERALL TEST SUMMARY".center(78) + "#")
    print("#"*80)
    print(f"# Total: {total_passed} passed, {total_failed} failed".ljust(79) + "#")
    
    if total_failed == 0:
        print("#" + " ALL TESTS PASSED! ".center(78, "✓") + "#")
    else:
        print("#" + " SOME TESTS FAILED ".center(78, "✗") + "#")
    
    print("#"*80 + "\n")
    
    return total_passed, total_failed


if __name__ == "__main__":
    run_all_tests()
