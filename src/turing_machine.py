"""
Turing Machine module for simulating Mealy Machines.

This module implements a single-tape Turing Machine that simulates
a Mealy Machine. This demonstrates how finite automata can be executed
on a more powerful computational model.

Theory of Computation Note:
- A Turing Machine is a computational model equivalent to any algorithm
- By simulating a Mealy Machine on a TM, we show that finite state machines
  are a subset of TM-computable problems
- The TM uses a tape to track:
  • Input symbols
  • Internal state
  • Output generated
  • Tape head position
"""

from typing import Dict, Tuple, List, Optional
from enum import Enum
from dataclasses import dataclass
from src.tape import Tape
from src.mealy_machine import MealyMachine


class TMTransitionType(Enum):
    """Types of Turing Machine transitions."""
    READ_INPUT = "read_input"
    WRITE_OUTPUT = "write_output"
    UPDATE_STATE = "update_state"
    MOVE_HEAD = "move_head"
    ACCEPT = "accept"
    REJECT = "reject"


@dataclass
class TMTransition:
    """Represents a single TM transition."""
    current_state: str
    read_symbol: str
    next_state: str
    write_symbol: str
    move_direction: str  # "L", "R", or "S" (stay)


class TuringMachine:
    """
    A Turing Machine that simulates a Mealy Machine.
    
    The TM works by:
    1. Reading input from the tape
    2. Maintaining the Mealy Machine's internal state
    3. Computing transitions and outputs
    4. Writing outputs to an output buffer
    5. Moving the tape head to process the next symbol
    
    This is a simplified deterministic TM designed specifically for
    simulating Mealy Machines.
    """
    
    def __init__(self, mealy_machine: MealyMachine, blank_symbol: str = "#"):
        """
        Initialize a Turing Machine for a Mealy Machine.
        
        Args:
            mealy_machine: The Mealy Machine to simulate
            blank_symbol: Symbol representing blank cells
        """
        self.mealy_machine = mealy_machine
        self.blank_symbol = blank_symbol
        self.tape: Optional[Tape] = None
        self.current_state = mealy_machine.initial_state
        self.output_buffer: str = ""
        self.step_count = 0
        self.execution_trace: List[Dict] = []
    
    def initialize(self, input_string: str) -> None:
        """
        Initialize the TM with input.
        
        Args:
            input_string: The string to process
        """
        self.tape = Tape(input_string, self.blank_symbol)
        self.current_state = self.mealy_machine.initial_state
        self.output_buffer = ""
        self.step_count = 0
        self.execution_trace = []
    
    def execute_step(self) -> Tuple[bool, str]:
        """
        Execute a single step of the TM.
        
        Returns:
            - Tuple of (is_halted, status_message)
            - is_halted: True if execution should stop
            - status_message: Description of what happened
        """
        if self.tape is None:
            return True, "Error: TM not initialized"
        
        # Read current symbol from tape
        input_symbol = self.tape.read()
        self.step_count += 1
        
        # Look up transition in Mealy Machine
        transition = self.mealy_machine.get_transition(self.current_state, input_symbol)
        
        if transition is None:
            # No defined transition
            return True, f"Execution halted: No transition from state '{self.current_state}' on '{input_symbol}'"
        
        next_state, output_symbol = transition
        
        # Record the trace
        trace_entry = {
            'step': self.step_count,
            'state': self.current_state,
            'input': input_symbol,
            'next_state': next_state,
            'output': output_symbol,
            'tape': self.tape.get_tape_content(),
            'head_pos': self.tape.head_position
        }
        self.execution_trace.append(trace_entry)
        
        # Update state
        self.current_state = next_state
        
        # Add output to output buffer
        if output_symbol != self.blank_symbol:
            self.output_buffer += output_symbol
        
        # Move tape head to the right (already passed blank, check for continuation)
        if input_symbol == self.blank_symbol:
            # We just processed the blank symbol, now check if next state has transition
            return True, "Input exhausted (processed blank symbol)"
        
        # Move tape head to the right for next symbol
        self.tape.move("R")
        
        return False, f"Step {self.step_count}: State={self.current_state}, Output so far={self.output_buffer}"
    
    def execute_full(self, max_steps: int = 10000) -> Tuple[str, bool, str]:
        """
        Execute the TM to completion.
        
        Args:
            max_steps: Maximum number of steps to prevent infinite loops
            
        Returns:
            Tuple of (output_string, success, final_status)
        """
        step_count = 0
        while step_count < max_steps:
            is_halted, status = self.execute_step()
            if is_halted:
                return self.output_buffer, True, status
            step_count += 1
        
        return self.output_buffer, False, f"Exceeded maximum steps ({max_steps})"
    
    def get_current_state(self) -> str:
        """Get the current state of the machine."""
        return self.current_state
    
    def get_output_buffer(self) -> str:
        """Get the accumulated output."""
        return self.output_buffer
    
    def get_tape_state(self) -> str:
        """Get the current tape state."""
        if self.tape is None:
            return "Uninitialized"
        return str(self.tape)
    
    def get_execution_trace(self) -> List[Dict]:
        """Get the execution trace."""
        return self.execution_trace
    
    def print_execution_trace(self) -> None:
        """Print a formatted execution trace."""
        print("\n=== Execution Trace ===")
        print(f"{'Step':<5} | {'State':<10} | {'Input':<7} | {'Next State':<12} | {'Output':<7} | {'Head Pos':<8}")
        print("-" * 75)
        
        for entry in self.execution_trace:
            print(
                f"{entry['step']:<5} | {entry['state']:<10} | "
                f"{entry['input']:<7} | {entry['next_state']:<12} | "
                f"{entry['output']:<7} | {entry['head_pos']:<8}"
            )
    
    def reset(self) -> None:
        """Reset the TM to its initial state."""
        self.tape = None
        self.current_state = self.mealy_machine.initial_state
        self.output_buffer = ""
        self.step_count = 0
        self.execution_trace = []
