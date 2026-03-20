"""
Visualization module for TM simulation.

This module provides both console-based and GUI-based visualization
of the Turing Machine simulation.
"""

from typing import List, Dict
from src.turing_machine import TuringMachine


class TraceVisualizer:
    """Visualizes the execution trace of a TM."""
    
    @staticmethod
    def print_trace_table(tm: TuringMachine, verbose: bool = False) -> None:
        """
        Print a formatted trace table.
        
        Args:
            tm: The TuringMachine instance
            verbose: If True, print additional details
        """
        trace = tm.get_execution_trace()
        
        if not trace:
            print("No execution trace available")
            return
        
        print("\n" + "=" * 100)
        print("EXECUTION TRACE TABLE".center(100))
        print("=" * 100)
        
        # Header
        if verbose:
            print(
                f"{'Step':<6} | {'State':<10} | {'Input':<7} | {'Output':<8} | "
                f"{'Next State':<12} | {'Tape Content':<20} | {'Head Pos':<8}"
            )
            print("-" * 100)
        else:
            print(
                f"{'Step':<6} | {'State':<10} | {'Input':<7} | {'Output':<8} | "
                f"{'Next State':<12}"
            )
            print("-" * 50)
        
        # Rows
        for entry in trace:
            if verbose:
                tape_content = entry['tape'][:20] + "..." if len(entry['tape']) > 20 else entry['tape']
                print(
                    f"{entry['step']:<6} | {entry['state']:<10} | {entry['input']:<7} | "
                    f"{entry['output']:<8} | {entry['next_state']:<12} | "
                    f"{tape_content:<20} | {entry['head_pos']:<8}"
                )
            else:
                print(
                    f"{entry['step']:<6} | {entry['state']:<10} | {entry['input']:<7} | "
                    f"{entry['output']:<8} | {entry['next_state']:<12}"
                )
        
        print("=" * 100)
    
    @staticmethod
    def print_summary(tm: TuringMachine, input_string: str) -> None:
        """
        Print a summary of the execution.
        
        Args:
            tm: The TuringMachine instance
            input_string: The input that was processed
        """
        trace = tm.get_execution_trace()
        
        print("\n" + "=" * 60)
        print("SIMULATION SUMMARY".center(60))
        print("=" * 60)
        print(f"Input String:        {input_string}")
        print(f"Output String:       {tm.get_output_buffer()}")
        print(f"Total Steps:         {len(trace)}")
        print(f"Final State:         {tm.get_current_state()}")
        print(f"Tape Content:        {tm.tape.get_tape_content() if tm.tape else 'N/A'}")
        print("=" * 60)
    
    @staticmethod
    def print_step_by_step(tm: TuringMachine) -> None:
        """
        Print step-by-step output during execution.
        
        Args:
            tm: The TuringMachine instance
        """
        print("\n" + "-" * 60)
        print("STEP-BY-STEP EXECUTION".center(60))
        print("-" * 60)
        
        for step, entry in enumerate(tm.get_execution_trace(), 1):
            print(f"\nStep {step}:")
            print(f"  Current State: {entry['state']}")
            print(f"  Input Symbol: {entry['input']}")
            print(f"  Next State: {entry['next_state']}")
            print(f"  Output: {entry['output']}")
            print(f"  Tape: {entry['tape']}")
            print(f"  Head Position: {entry['head_pos']}")


class TransitionTablePrinter:
    """Prints the transition table in various formats."""
    
    @staticmethod
    def print_mealy_table(machine) -> None:
        """Print Mealy Machine transition table."""
        machine.print_transition_table()
    
    @staticmethod
    def print_state_output_table(tm: TuringMachine) -> None:
        """
        Print a table showing state-output relationships.
        
        Args:
            tm: The TuringMachine instance
        """
        trace = tm.get_execution_trace()
        states_outputs = {}
        
        for entry in trace:
            state = entry['state']
            output = entry['output']
            
            if state not in states_outputs:
                states_outputs[state] = []
            if output != "#":
                states_outputs[state].append(output)
        
        print("\n" + "=" * 50)
        print("STATE-OUTPUT MAPPING".center(50))
        print("=" * 50)
        
        for state in sorted(states_outputs.keys()):
            outputs = "".join(states_outputs[state])
            print(f"{state:<15} → {outputs}")
        
        print("=" * 50)


class InteractiveSimulator:
    """Provides interactive step-by-step simulation."""
    
    def __init__(self, tm: TuringMachine, input_string: str):
        """
        Initialize the interactive simulator.
        
        Args:
            tm: The TuringMachine instance
            input_string: The input to process
        """
        self.tm = tm
        self.input_string = input_string
        self.current_step = 0
        
        tm.initialize(input_string)
    
    def run_interactive(self) -> None:
        """Run interactive step-by-step simulation."""
        print(f"\n{'='*60}")
        print(f"INTERACTIVE MEALY MACHINE SIMULATOR".center(60))
        print(f"{'='*60}")
        print(f"Input String: {self.input_string}")
        print(f"Commands: [space/enter] next step, [s] skip to end, [q] quit")
        print(f"{'='*60}\n")
        
        while True:
            is_halted, status = self.tm.execute_step()
            
            trace = self.tm.get_execution_trace()
            if trace:
                entry = trace[-1]
                print(f"Step {entry['step']}:")
                print(f"  State: {entry['state']:.<20} Input: {entry['input']}")
                print(f"  Next: {entry['next_state']:.<20} Output: {entry['output']}")
                print(f"  Output Buffer: {self.tm.get_output_buffer()}")
            
            if is_halted:
                print(f"\nExecution Halted: {status}")
                break
            
            cmd = input("\n[Enter] Next, [s] Skip to end, [q] Quit: ").lower().strip()
            if cmd == 'q':
                print("Execution stopped by user")
                break
            elif cmd == 's':
                _, _, final_status = self.tm.execute_full()
                print(f"\nSkipped to end")
                print(f"Final Status: {final_status}")
                break
            print()
