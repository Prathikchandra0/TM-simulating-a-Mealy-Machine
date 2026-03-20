"""
Configuration loader for Mealy Machines.

This module loads machine definitions from JSON files, making it easy to
define and test different machines without modifying code.
"""

import json
from typing import Dict, Set, Any
from src.mealy_machine import MealyMachine


class MachineConfigError(Exception):
    """Exception raised for configuration errors."""
    pass


class ConfigLoader:
    """Loads Mealy Machine configurations from JSON files."""
    
    @staticmethod
    def load_from_file(filepath: str) -> MealyMachine:
        """
        Load a Mealy Machine configuration from a JSON file.
        
        JSON Structure:
        {
            "name": "Machine Name",
            "states": ["q0", "q1", ...],
            "input_alphabet": ["0", "1", ...],
            "output_alphabet": ["0", "1", ...],
            "initial_state": "q0",
            "blank_symbol": "#",
            "transitions": [
                {
                    "from": "q0",
                    "input": "0",
                    "to": "q1",
                    "output": "0"
                },
                ...
            ]
        }
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            MealyMachine instance
            
        Raises:
            MachineConfigError: If configuration is invalid
        """
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            raise MachineConfigError(f"Configuration file not found: {filepath}")
        except json.JSONDecodeError:
            raise MachineConfigError(f"Invalid JSON in configuration file: {filepath}")
        
        return ConfigLoader._parse_config(config)
    
    @staticmethod
    def _parse_config(config: Dict[str, Any]) -> MealyMachine:
        """
        Parse a configuration dictionary into a MealyMachine.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            MealyMachine instance
            
        Raises:
            MachineConfigError: If configuration is invalid
        """
        # Required fields
        required_fields = ['states', 'input_alphabet', 'output_alphabet', 
                          'initial_state', 'transitions']
        
        for field in required_fields:
            if field not in config:
                raise MachineConfigError(f"Missing required field: {field}")
        
        states: Set[str] = set(config['states'])
        input_alphabet: Set[str] = set(config['input_alphabet'])
        output_alphabet: Set[str] = set(config['output_alphabet'])
        initial_state: str = config['initial_state']
        blank_symbol: str = config.get('blank_symbol', '#')
        
        # Create the machine
        machine = MealyMachine(states, input_alphabet, output_alphabet, 
                             initial_state, blank_symbol)
        
        # Add transitions
        transitions = config['transitions']
        if not isinstance(transitions, list):
            raise MachineConfigError("Transitions must be a list")
        
        for transition in transitions:
            required_trans_fields = ['from', 'input', 'to', 'output']
            for field in required_trans_fields:
                if field not in transition:
                    raise MachineConfigError(
                        f"Transition missing required field: {field}"
                    )
            
            try:
                machine.add_transition(
                    transition['from'],
                    transition['input'],
                    transition['to'],
                    transition['output']
                )
            except ValueError as e:
                raise MachineConfigError(f"Invalid transition: {e}")
        
        return machine
    
    @staticmethod
    def load_from_dict(config: Dict[str, Any]) -> MealyMachine:
        """
        Load a Mealy Machine configuration from a dictionary.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            MealyMachine instance
        """
        return ConfigLoader._parse_config(config)
    
    @staticmethod
    def save_to_file(machine: MealyMachine, filepath: str, name: str = "Mealy Machine") -> None:
        """
        Save a Mealy Machine configuration to a JSON file.
        
        Args:
            machine: The MealyMachine to save
            filepath: Path where to save the JSON file
            name: Name/description for the machine
        """
        config = {
            "name": name,
            "states": sorted(list(machine.states)),
            "input_alphabet": sorted(list(machine.input_alphabet)),
            "output_alphabet": sorted(list(machine.output_alphabet)),
            "initial_state": machine.initial_state,
            "blank_symbol": machine.blank_symbol,
            "transitions": [
                {
                    "from": from_state,
                    "input": input_sym,
                    "to": to_state,
                    "output": output_sym
                }
                for (from_state, input_sym), (to_state, output_sym) 
                in sorted(machine.transitions.items())
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
