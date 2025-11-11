"""
Turing Machine Simulator

This script simulates a Turing machine with configurable states, transitions,
and tape operations.
"""


class TuringMachine:
    """
    A Turing Machine simulator.
    
    The machine consists of:
    - An infinite tape (represented as a list with dynamic expansion)
    - A read/write head that can move left or right
    - A set of states with transitions
    - An initial state and accept/reject states
    """
    
    def __init__(self, states, alphabet, tape_alphabet, transitions, 
                 initial_state, accept_states, reject_states, blank_symbol='_'):
        """
        Initialize the Turing Machine.
        
        Args:
            states: Set of state names
            alphabet: Input alphabet (symbols that can appear in input)
            tape_alphabet: Tape alphabet (includes alphabet + blank symbol)
            transitions: Dictionary mapping (state, symbol) -> (new_state, write_symbol, direction)
            initial_state: Starting state
            accept_states: Set of accepting states
            reject_states: Set of rejecting states
            blank_symbol: Symbol representing blank cells on tape
        """
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.blank_symbol = blank_symbol
        
        # Machine state
        self.tape = []
        self.head_position = 0
        self.current_state = initial_state
        self.steps = 0
        
    def load_input(self, input_string):
        """Load input string onto the tape."""
        self.tape = list(input_string) if input_string else [self.blank_symbol]
        self.head_position = 0
        self.current_state = self.initial_state
        self.steps = 0
        
    def step(self):
        """
        Execute one step of the Turing machine.
        
        Returns:
            True if machine continues, False if halted (accepted or rejected)
        """
        # Extend tape if head is at boundary
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
            
        # Read current symbol
        current_symbol = self.tape[self.head_position]
        
        # Check if we're in accept or reject state
        if self.current_state in self.accept_states:
            return False
        if self.current_state in self.reject_states:
            return False
            
        # Get transition
        transition_key = (self.current_state, current_symbol)
        if transition_key not in self.transitions:
            # No transition defined - implicit rejection
            self.current_state = list(self.reject_states)[0] if self.reject_states else 'REJECT'
            return False
            
        new_state, write_symbol, direction = self.transitions[transition_key]
        
        # Execute transition
        self.tape[self.head_position] = write_symbol
        self.current_state = new_state
        
        # Move head
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'N' or any other value means no movement
        
        self.steps += 1
        return True
        
    def run(self, input_string, max_steps=10000, verbose=False):
        """
        Run the Turing machine on an input string.
        
        Args:
            input_string: Input to process
            max_steps: Maximum steps before halting
            verbose: Print each step
            
        Returns:
            Tuple of (accepted: bool, steps: int, final_tape: str)
        """
        self.load_input(input_string)
        
        if verbose:
            print(f"Initial: {self.get_tape_string()}")
            print(f"State: {self.current_state}, Head: {self.head_position}\n")
        
        while self.steps < max_steps:
            if not self.step():
                break
                
            if verbose:
                print(f"Step {self.steps}: {self.get_tape_string()}")
                print(f"State: {self.current_state}, Head: {self.head_position}\n")
        
        accepted = self.current_state in self.accept_states
        final_tape = self.get_tape_string()
        
        if verbose:
            status = "ACCEPTED" if accepted else "REJECTED"
            print(f"Result: {status}")
            print(f"Final tape: {final_tape}")
            print(f"Total steps: {self.steps}")
        
        return accepted, self.steps, final_tape
        
    def get_tape_string(self):
        """Get string representation of tape with head position marker."""
        tape_str = ''.join(self.tape)
        # Trim trailing blank symbols for display
        tape_str = tape_str.rstrip(self.blank_symbol)
        if not tape_str:
            tape_str = self.blank_symbol
        return tape_str


def example_binary_increment():
    """
    Example: Turing machine that increments a binary number.
    Input: Binary number (e.g., '1011')
    Output: Binary number + 1 (e.g., '1100')
    """
    states = {'start', 'seek_end', 'carry', 'done', 'reject'}
    alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', '_'}
    blank = '_'
    
    transitions = {
        # Move to the rightmost digit
        ('start', '0'): ('seek_end', '0', 'R'),
        ('start', '1'): ('seek_end', '1', 'R'),
        ('start', '_'): ('reject', '_', 'N'),
        
        ('seek_end', '0'): ('seek_end', '0', 'R'),
        ('seek_end', '1'): ('seek_end', '1', 'R'),
        ('seek_end', '_'): ('carry', '_', 'L'),
        
        # Add 1 with carry
        ('carry', '0'): ('done', '1', 'N'),
        ('carry', '1'): ('carry', '0', 'L'),
        ('carry', '_'): ('done', '1', 'N'),
    }
    
    initial_state = 'start'
    accept_states = {'done'}
    reject_states = {'reject'}
    
    tm = TuringMachine(states, alphabet, tape_alphabet, transitions,
                      initial_state, accept_states, reject_states, blank)
    
    print("=" * 60)
    print("TURING MACHINE: Binary Increment")
    print("=" * 60)
    
    test_cases = ['1', '10', '11', '1011', '1111']
    
    for test in test_cases:
        print(f"\nInput: {test}")
        accepted, steps, result = tm.run(test, verbose=False)
        print(f"Output: {result}")
        print(f"Steps: {steps}, Status: {'ACCEPTED' if accepted else 'REJECTED'}")


def example_palindrome_checker():
    """
    Example: Turing machine that checks if a binary string is a palindrome.
    Input: Binary string (e.g., '1001')
    Output: Accepts if palindrome, rejects otherwise
    """
    states = {'start', 'check_0', 'check_1', 'move_left', 'move_right', 
              'accept', 'reject'}
    alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', 'X', '_'}
    blank = '_'
    
    transitions = {
        # Start state - mark first symbol
        ('start', '0'): ('check_0', 'X', 'R'),
        ('start', '1'): ('check_1', 'X', 'R'),
        ('start', 'X'): ('accept', 'X', 'N'),
        ('start', '_'): ('accept', '_', 'N'),
        
        # Move to end for checking '0'
        ('check_0', '0'): ('check_0', '0', 'R'),
        ('check_0', '1'): ('check_0', '1', 'R'),
        ('check_0', 'X'): ('check_0', 'X', 'R'),
        ('check_0', '_'): ('move_left', '_', 'L'),
        
        # Move to end for checking '1'
        ('check_1', '0'): ('check_1', '0', 'R'),
        ('check_1', '1'): ('check_1', '1', 'R'),
        ('check_1', 'X'): ('check_1', 'X', 'R'),
        ('check_1', '_'): ('move_left', '_', 'L'),
        
        # Move left to find last unmarked symbol
        ('move_left', '0'): ('move_right', 'X', 'L'),
        ('move_left', '1'): ('move_right', 'X', 'L'),
        ('move_left', 'X'): ('move_left', 'X', 'L'),
        
        # Move right back to start
        ('move_right', '0'): ('move_right', '0', 'L'),
        ('move_right', '1'): ('move_right', '1', 'L'),
        ('move_right', 'X'): ('move_right', 'X', 'L'),
        ('move_right', '_'): ('start', '_', 'R'),
    }
    
    initial_state = 'start'
    accept_states = {'accept'}
    reject_states = {'reject'}
    
    tm = TuringMachine(states, alphabet, tape_alphabet, transitions,
                      initial_state, accept_states, reject_states, blank)
    
    print("\n" + "=" * 60)
    print("TURING MACHINE: Palindrome Checker")
    print("=" * 60)
    
    test_cases = ['1', '11', '101', '1001', '1101', '11011', '10101']
    
    for test in test_cases:
        print(f"\nInput: {test}")
        accepted, steps, result = tm.run(test, verbose=False)
        is_palindrome = test == test[::-1]
        status = "✓ CORRECT" if accepted == is_palindrome else "✗ WRONG"
        print(f"Expected: {is_palindrome}, Got: {accepted} {status}")
        print(f"Steps: {steps}")


def main():
    """Run example Turing machines."""
    print("\n🤖 TURING MACHINE SIMULATOR 🤖\n")
    
    # Example 1: Binary increment
    example_binary_increment()
    
    # Example 2: Palindrome checker
    example_palindrome_checker()
    
    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()