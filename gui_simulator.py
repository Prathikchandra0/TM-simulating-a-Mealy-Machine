"""
GUI-based Mealy Machine Turing Machine Simulator.

This module provides a Tkinter-based graphical interface for simulating
Mealy Machines using a Turing Machine. Users can:
- Load predefined machines from JSON
- Define custom machines
- Run step-by-step simulations
- View execution traces and outputs
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.mealy_machine import MealyMachine
from src.turing_machine import TuringMachine
from src.config_loader import ConfigLoader, MachineConfigError
from src.visualizer import TraceVisualizer, InteractiveSimulator


class MealyMachineGUI:
    """Main GUI application for Mealy Machine simulation."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Mealy Machine Turing Machine Simulator")
        self.root.geometry("1000x700")
        
        self.tm = None
        self.mealy_machine = None
        self.current_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Load Machine
        self.setup_load_tab()
        
        # Tab 2: Simulation
        self.setup_simulation_tab()
        
        # Tab 3: Results
        self.setup_results_tab()
        
        # Tab 4: Documentation
        self.setup_documentation_tab()
    
    def setup_load_tab(self):
        """Set up the machine loading tab."""
        load_frame = ttk.Frame(self.notebook)
        self.notebook.add(load_frame, text="Load Machine")
        
        # File selection
        file_frame = ttk.LabelFrame(load_frame, text="Load from File", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            file_frame,
            text="Browse and Load JSON Machine",
            command=self.load_machine_file
        ).pack(pady=5)
        
        # Preset machines
        preset_frame = ttk.LabelFrame(load_frame, text="Load Preset Machines", padding=10)
        preset_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            preset_frame,
            text="Binary Incrementer",
            command=lambda: self.load_preset("machines/binary_incrementer.json")
        ).pack(pady=5)
        
        ttk.Button(
            preset_frame,
            text="Parity Checker",
            command=lambda: self.load_preset("machines/parity_checker.json")
        ).pack(pady=5)
        
        # Machine info
        info_frame = ttk.LabelFrame(load_frame, text="Machine Information", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.machine_info_text = tk.Text(info_frame, height=15, width=80)
        self.machine_info_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.machine_info_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.machine_info_text.config(yscrollcommand=scrollbar.set)
    
    def setup_simulation_tab(self):
        """Set up the simulation tab."""
        sim_frame = ttk.Frame(self.notebook)
        self.notebook.add(sim_frame, text="Simulate")
        
        # Input frame
        input_frame = ttk.LabelFrame(sim_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Input String:").pack()
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.pack(pady=5)
        
        # Simulation options
        options_frame = ttk.LabelFrame(sim_frame, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.verbose_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Verbose Mode (Show detailed trace)",
            variable=self.verbose_var
        ).pack()
        
        self.step_by_step_var = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame,
            text="Step-by-Step Interactive Mode",
            variable=self.step_by_step_var
        ).pack()
        
        # Buttons
        button_frame = ttk.Frame(sim_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            button_frame,
            text="Run Simulation",
            command=self.run_simulation
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Run Interactive",
            command=self.run_interactive
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_simulation
        ).pack(side=tk.LEFT, padx=5)
    
    def setup_results_tab(self):
        """Set up the results tab."""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Results")
        
        # Results display
        self.results_text = tk.Text(results_frame, height=30, width=100)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.results_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
    
    def setup_documentation_tab(self):
        """Set up the documentation tab."""
        doc_frame = ttk.Frame(self.notebook)
        self.notebook.add(doc_frame, text="Help")
        
        doc_text = tk.Text(doc_frame, height=30, width=100, wrap=tk.WORD)
        doc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        documentation = """
MEALY MACHINE TURING MACHINE SIMULATOR
=====================================

WHAT IS A MEALY MACHINE?
------------------------
A Mealy Machine is a finite state machine where:
- Output depends on BOTH current state AND input symbol
- Output is produced during state transitions
- Formally: δ(state, input) → (next_state, output)

WHAT IS A TURING MACHINE?
-------------------------
A Turing Machine is a theoretical computational model with:
- An infinite tape divided into cells (readable/writable)
- A tape head that can move left or right
- A state machine that controls transitions
- Equivalent computational power to any real computer

WHY SIMULATE MEALY MACHINES WITH TURING MACHINES?
--------------------------------------------------
This simulator demonstrates:
1. That finite automata are executable on more powerful models
2. How to encode finite state machines in TM transitions
3. The hierarchy of automata theory (DFA → Mealy → TM)

HOW TO USE THIS SIMULATOR
-------------------------

1. LOAD A MACHINE:
   - Use the "Load Machine" tab
   - Choose from preset machines or load from JSON
   - View the transition table and machine details

2. PROVIDE INPUT:
   - Go to "Simulate" tab
   - Enter input string in the input field
   - Each symbol must be in the input alphabet

3. RUN SIMULATION:
   - "Run Simulation" executes the machine step-by-step
   - Results show in the "Results" tab
   - View complete execution trace

4. INTERACTIVE MODE:
   - "Run Interactive" allows manual step-by-step control
   - Observe machine behavior in detail

OUTPUT INTERPRETATION
--------------------
- Current State: The machine's current state
- Input Symbol: The symbol being read from tape
- Output: Symbol produced in this transition
- Tape Content: The full tape after this step
- Head Position: Position of the read/write head

EXAMPLE: BINARY INCREMENTER
---------------------------
Increments a binary number by 1
Input: "11"
- Step 1: Read '1' → Output '1', stay in q0
- Step 2: Read '1' → Output '1', stay in q0
- Step 3: Read '#' → Output '1', go to q1 (this is +1)
Output: "111" (3 in binary, which is 2+1)

EXAMPLE: PARITY CHECKER
-----------------------
Outputs 0 if even number of 1s, 1 if odd
Input: "1101"
- Counts the 1s (three 1s = odd)
Output: "1" (indicates odd parity)

FILES AND CONFIGURATION
-----------------------
Machines are defined in JSON format:
{
    "name": "Machine Name",
    "states": ["q0", "q1"],
    "input_alphabet": ["0", "1"],
    "output_alphabet": ["0", "1"],
    "initial_state": "q0",
    "blank_symbol": "#",
    "transitions": [
        {"from": "q0", "input": "0", "to": "q1", "output": "1"},
        ...
    ]
}

THEORY OF COMPUTATION CONCEPTS
------------------------------
- DFA (Deterministic Finite Automaton): Recognizes regular languages
- Mealy Machine: DFA + output function
- moore Machine: DFA with state-based output
- Turing Machine: Most powerful model, computes partially recursive functions

This simulator bridges the gap between finite automata and Turing computation!
"""
        
        doc_text.insert(1.0, documentation)
        doc_text.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(doc_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        doc_text.config(yscrollcommand=scrollbar.set)
    
    def load_machine_file(self):
        """Load a machine from a selected file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.mealy_machine = ConfigLoader.load_from_file(filepath)
                self.tm = TuringMachine(self.mealy_machine)
                self.current_file = filepath
                self.display_machine_info()
                messagebox.showinfo("Success", f"Machine loaded from:\n{filepath}")
            except MachineConfigError as e:
                messagebox.showerror("Error", f"Failed to load machine:\n{e}")
    
    def load_preset(self, relative_path):
        """Load a preset machine."""
        # Construct the path relative to the script location
        script_dir = Path(__file__).parent
        filepath = script_dir / relative_path
        
        try:
            self.mealy_machine = ConfigLoader.load_from_file(str(filepath))
            self.tm = TuringMachine(self.mealy_machine)
            self.current_file = str(filepath)
            self.display_machine_info()
            messagebox.showinfo("Success", f"Machine loaded successfully!")
        except MachineConfigError as e:
            messagebox.showerror("Error", f"Failed to load machine:\n{e}")
    
    def display_machine_info(self):
        """Display information about the loaded machine."""
        if self.mealy_machine is None:
            return
        
        self.machine_info_text.config(state=tk.NORMAL)
        self.machine_info_text.delete(1.0, tk.END)
        
        info = f"MEALY MACHINE INFORMATION\n"
        info += "=" * 60 + "\n\n"
        info += f"States: {sorted(self.mealy_machine.states)}\n\n"
        info += f"Input Alphabet: {sorted(self.mealy_machine.input_alphabet)}\n\n"
        info += f"Output Alphabet: {sorted(self.mealy_machine.output_alphabet)}\n\n"
        info += f"Initial State: {self.mealy_machine.initial_state}\n\n"
        info += f"Blank Symbol: {self.mealy_machine.blank_symbol}\n\n"
        
        info += "TRANSITION TABLE\n"
        info += "-" * 60 + "\n"
        info += f"{'State':<10} | {'Input':<8} | {'Next State':<12} | {'Output':<8}\n"
        info += "-" * 60 + "\n"
        
        for (state, input_sym), (next_state, output_sym) in sorted(self.mealy_machine.transitions.items()):
            info += f"{state:<10} | {input_sym:<8} | {next_state:<12} | {output_sym:<8}\n"
        
        self.machine_info_text.insert(tk.END, info)
        self.machine_info_text.config(state=tk.DISABLED)
    
    def run_simulation(self):
        """Run the simulation."""
        if self.tm is None:
            messagebox.showerror("Error", "Please load a machine first!")
            return
        
        input_string = self.input_entry.get()
        
        if not input_string:
            messagebox.showerror("Error", "Please enter an input string!")
            return
        
        # Validate input
        for symbol in input_string:
            if symbol not in self.mealy_machine.input_alphabet:
                messagebox.showerror(
                    "Error",
                    f"Invalid symbol '{symbol}' not in input alphabet!\n"
                    f"Valid symbols: {sorted(self.mealy_machine.input_alphabet)}"
                )
                return
        
        # Run simulation
        self.tm.reset()
        self.tm.initialize(input_string)
        output, success, status = self.tm.execute_full()
        
        # Display results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        results = "SIMULATION RESULTS\n"
        results += "=" * 80 + "\n\n"
        results += f"Input String:    {input_string}\n"
        results += f"Output String:   {output}\n"
        results += f"Total Steps:     {len(self.tm.execution_trace)}\n"
        results += f"Final State:     {self.tm.current_state}\n"
        results += f"Status:          {status}\n"
        results += f"Success:         {success}\n"
        results += "\n" + "=" * 80 + "\n"
        results += "EXECUTION TRACE\n"
        results += "=" * 80 + "\n"
        results += f"{'Step':<6} | {'State':<10} | {'Input':<7} | {'Output':<8} | {'Next State':<12}\n"
        results += "-" * 80 + "\n"
        
        for entry in self.tm.execution_trace:
            results += (
                f"{entry['step']:<6} | {entry['state']:<10} | {entry['input']:<7} | "
                f"{entry['output']:<8} | {entry['next_state']:<12}\n"
            )
        
        self.results_text.insert(tk.END, results)
        self.results_text.config(state=tk.DISABLED)
    
    def run_interactive(self):
        """Run interactive simulation."""
        if self.tm is None:
            messagebox.showerror("Error", "Please load a machine first!")
            return
        
        input_string = self.input_entry.get()
        
        if not input_string:
            messagebox.showerror("Error", "Please enter an input string!")
            return
        
        # Validate input
        for symbol in input_string:
            if symbol not in self.mealy_machine.input_alphabet:
                messagebox.showerror(
                    "Error",
                    f"Invalid symbol '{symbol}' not in input alphabet!"
                )
                return
        
        # Reset and run interactive
        self.tm.reset()
        simulator = InteractiveSimulator(self.tm, input_string)
        
        # Hide GUI temporarily and run interactive simulation
        self.root.withdraw()
        simulator.run_interactive()
        self.root.deiconify()
    
    def clear_simulation(self):
        """Clear the simulation."""
        self.input_entry.delete(0, tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MealyMachineGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
