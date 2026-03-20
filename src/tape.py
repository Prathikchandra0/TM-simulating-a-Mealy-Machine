"""
Tape module for Turing Machine simulation.

This module represents the infinite tape of a Turing Machine with symbols.
The tape can be read from and written to, and a head pointer can move left and right.
"""

from typing import List, Optional


class Tape:
    """
    Represents the tape of a Turing Machine.
    
    The tape is implemented as a list that can grow dynamically.
    A blank symbol is used to represent empty cells.
    """
    
    def __init__(self, input_string: str, blank_symbol: str = "#"):
        """
        Initialize the tape with an input string.
        
        Args:
            input_string: The initial content of the tape
            blank_symbol: Symbol to represent blank cells (default: "#")
        """
        self.blank_symbol = blank_symbol
        self.tape: List[str] = list(input_string) if input_string else []
        self.head_position: int = 0
    
    def read(self) -> str:
        """
        Read the symbol at the current head position.
        
        Returns:
            The symbol at the head position, or blank_symbol if out of bounds
        """
        if 0 <= self.head_position < len(self.tape):
            return self.tape[self.head_position]
        return self.blank_symbol
    
    def write(self, symbol: str) -> None:
        """
        Write a symbol at the current head position.
        
        Args:
            symbol: The symbol to write
        """
        # Expand tape to the right if needed
        while self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
        
        # Expand tape to the left if needed (shift all elements)
        while self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position += 1
        
        self.tape[self.head_position] = symbol
    
    def move(self, direction: str) -> None:
        """
        Move the head left or right.
        
        Args:
            direction: "L" for left, "R" for right, "S" for stay
        """
        if direction == "L":
            self.head_position -= 1
        elif direction == "R":
            self.head_position += 1
        # "S" means stay, so no change
    
    def get_tape_content(self) -> str:
        """Get the current content of the tape as a string."""
        return "".join(self.tape)
    
    def reset(self, input_string: str = "") -> None:
        """
        Reset the tape with new content.
        
        Args:
            input_string: New content for the tape
        """
        self.tape = list(input_string) if input_string else []
        self.head_position = 0
    
    def __str__(self) -> str:
        """String representation of the tape state."""
        tape_str = "".join(self.tape) if self.tape else "ε"
        return f"Tape: {tape_str} | Head: [{self.head_position}]"
    
    def get_tape_visualization(self) -> str:
        """
        Get a visual representation of the tape with the head position.
        
        Returns:
            A formatted string showing the tape and head position
        """
        if not self.tape:
            return "[ ]"
        
        tape_display = "[ " + " ] [ ".join(self.tape) + " ]"
        head_display = "\n" + " " * (self.head_position * 4 + 2) + "^"
        
        return tape_display + head_display
