"""
Mealy Machine module.

A Mealy Machine is a finite state machine where the output depends on 
both the current state and the input symbol. This forms the basis for our
Turing Machine simulation.

Theory of Computation Note:
- Mealy machines are more expressive than Moore machines
- Transition function: δ(state, input) → (next_state, output)
- Output is produced during transitions, not in states
"""

from typing import Dict, Tuple, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class MealyTransition:
    """Represents a single transition in a Mealy Machine."""
    current_state: str
    input_symbol: str
    next_state: str
    output_symbol: str
    
    def __repr__(self) -> str:
        return f"({self.current_state}, {self.input_symbol}) → ({self.next_state}, {self.output_symbol})"


class MealyMachine:
    """
    A Mealy Machine implementation.
    
    A Mealy Machine is defined by:
    - Q: Set of states
    - Σ: Input alphabet
    - Δ: Output alphabet
    - δ: Transition function (state, input) → (next_state, output)
    - q0: Initial state
    """
    
    def __init__(
        self,
        states: Set[str],
        input_alphabet: Set[str],
        output_alphabet: Set[str],
        initial_state: str,
        blank_symbol: str = "#"
    ):
        """
        Initialize a Mealy Machine.
        
        Args:
            states: Set of state names
            input_alphabet: Set of input symbols
            output_alphabet: Set of output symbols
            initial_state: The initial state
            blank_symbol: Symbol for blank/end of input
        """
        self.states = states
        self.input_alphabet = input_alphabet
        self.output_alphabet = output_alphabet
        self.initial_state = initial_state
        self.blank_symbol = blank_symbol
        
        # Transition function: (state, input) → (next_state, output)
        self.transitions: Dict[Tuple[str, str], Tuple[str, str]] = {}
        
        # Validation
        if initial_state not in states:
            raise ValueError(f"Initial state '{initial_state}' not in states")
    
    def add_transition(
        self,
        current_state: str,
        input_symbol: str,
        next_state: str,
        output_symbol: str
    ) -> None:
        """
        Add a transition to the machine.
        
        Args:
            current_state: Current state
            input_symbol: Input symbol
            next_state: Next state
            output_symbol: Output symbol produced
            
        Raises:
            ValueError: If states or symbols are not in the defined sets
        """
        if current_state not in self.states:
            raise ValueError(f"State '{current_state}' not in defined states")
        if next_state not in self.states:
            raise ValueError(f"State '{next_state}' not in defined states")
        if input_symbol not in self.input_alphabet and input_symbol != self.blank_symbol:
            raise ValueError(f"Input symbol '{input_symbol}' not in input alphabet")
        if output_symbol not in self.output_alphabet and output_symbol != self.blank_symbol:
            raise ValueError(f"Output symbol '{output_symbol}' not in output alphabet")
        
        key = (current_state, input_symbol)
        if key in self.transitions:
            print(f"Warning: Overwriting existing transition {key}")
        
        self.transitions[key] = (next_state, output_symbol)
    
    def get_transition(self, state: str, input_symbol: str) -> Optional[Tuple[str, str]]:
        """
        Get the transition for a given state and input.
        
        Args:
            state: Current state
            input_symbol: Input symbol
            
        Returns:
            Tuple of (next_state, output_symbol) or None if no transition exists
        """
        return self.transitions.get((state, input_symbol))
    
    def is_defined_transition(self, state: str, input_symbol: str) -> bool:
        """Check if a transition is defined for the given state and input."""
        return (state, input_symbol) in self.transitions
    
    def get_current_state(self) -> str:
        """Get the initial state (for tracking purposes)."""
        return self.initial_state
    
    def get_all_transitions(self) -> List[MealyTransition]:
        """Get all transitions in the machine."""
        transitions = []
        for (state, input_sym), (next_state, output_sym) in self.transitions.items():
            transitions.append(
                MealyTransition(state, input_sym, next_state, output_sym)
            )
        return transitions
    
    def __repr__(self) -> str:
        """String representation of the Mealy Machine."""
        return (
            f"MealyMachine(\n"
            f"  States: {self.states},\n"
            f"  Input Alphabet: {self.input_alphabet},\n"
            f"  Output Alphabet: {self.output_alphabet},\n"
            f"  Initial State: {self.initial_state},\n"
            f"  Transitions: {len(self.transitions)}\n"
            f")"
        )
    
    def print_transition_table(self) -> None:
        """Print a formatted transition table."""
        print("\n=== Mealy Machine Transition Table ===")
        print(f"{'State':<10} | {'Input':<8} | {'Next State':<12} | {'Output':<8}")
        print("-" * 50)
        
        for (state, input_sym), (next_state, output_sym) in sorted(self.transitions.items()):
            print(f"{state:<10} | {input_sym:<8} | {next_state:<12} | {output_sym:<8}")
