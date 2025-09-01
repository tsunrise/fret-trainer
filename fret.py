#!/usr/bin/env python3
import random
import sys
import termios
import tty
import os
from colorama import Fore, Style, init

init(autoreset=True)

class FretTrainer:
    def __init__(self):
        self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.strings = ['E', 'A', 'D', 'G', 'B', 'E'][::-1]  # Standard tuning (high to low)
        self.history = []  # Store exercise history
        self.history_index = -1  # Current position in history (-1 means no history yet)
        self.max_history = 1024
    
    def enter_alternate_screen(self):
        """Enter alternate screen buffer"""
        print("\033[?1049h", end="")
        sys.stdout.flush()
    
    def exit_alternate_screen(self):
        """Exit alternate screen buffer"""
        print("\033[?1049l", end="")
        sys.stdout.flush()
    
    def clear_screen(self):
        """Clear the current screen"""
        print("\033[2J\033[H", end="")
        sys.stdout.flush()

    def get_single_key(self):
        """Get a single key press without pressing Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1)
            # Handle arrow keys (multi-byte sequences)
            if ord(key) == 27:  # ESC sequence
                key += sys.stdin.read(2)  # Read remaining bytes
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def show_header(self):
        print("="*50)
        print("🎸 GUITAR FRET TRAINER 🎸")
        print("="*50)
    
    def add_to_history(self, exercise_type, content):
        """Add an exercise to history, maintaining max size"""
        exercise = {'type': exercise_type, 'content': content}
        
        # If we're not at the end of history, remove everything after current position
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add new exercise
        self.history.append(exercise)
        
        # Maintain max history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1
        
        # Update index to point to new exercise
        self.history_index = len(self.history) - 1
    
    def navigate_history(self, direction):
        """Navigate through history. direction: 1 for forward, -1 for back"""
        if direction == -1 and self.history_index > 0:
            self.history_index -= 1
            return True
        elif direction == 1 and self.history_index < len(self.history) - 1:
            self.history_index += 1
            return True
        return False
    
    def show_current_exercise(self):
        """Display the current exercise from history"""
        if self.history_index >= 0 and self.history_index < len(self.history):
            exercise = self.history[self.history_index]
            self.clear_screen()
            
            if exercise['type'] == 'location':
                print(f"\n{Fore.YELLOW}{Style.BRIGHT}{exercise['content']}{Style.RESET_ALL}")
            else:  # inverse-location
                for i, (string_name, fret_pos) in enumerate(exercise['content']):
                    self.draw_string_fretboard(fret_pos, i+1)
            self.show_navigation()
    
    def show_navigation(self):
        """Display navigation options with counts"""
        back_count = self.history_index
        next_count = len(self.history) - 1 - self.history_index
        
        back_text = f"\033[4mB\033[0mack ({back_count})" if back_count > 0 else f"{Fore.WHITE}Back (0){Style.RESET_ALL}"
        next_text = f"\033[4mN\033[0mext ({next_count})" if next_count > 0 else f"{Fore.WHITE}Next (0){Style.RESET_ALL}"
        
        # Determine current exercise type for dynamic key bindings
        current_type = None
        if self.history_index >= 0 and self.history_index < len(self.history):
            current_type = self.history[self.history_index]['type']
        
        # Dynamic key bindings based on current exercise
        if current_type == 'location':
            note_to_fret_text = "Note to Fret Exercise (Z | Space)"
            fret_to_note_text = "Fret to Note Exercise (X)"
        elif current_type == 'inverse-location':
            note_to_fret_text = "Note to Fret Exercise (Z)"
            fret_to_note_text = "Fret to Note Exercise (X | Space)"
        else:
            note_to_fret_text = "Note to Fret Exercise (Z)"
            fret_to_note_text = "Fret to Note Exercise (X)"
        
        print(f"\n{back_text} | {next_text}")
        print(f"{note_to_fret_text}")
        print(f"{fret_to_note_text}")
        print(f"Exit (Ctrl+C)")
        print()
    
    def note_to_fret_exercise(self, from_history=False):
        """Generate random sequence of 7 unique notes"""
        if not from_history:
            shuffled_notes = self.notes.copy()
            random.shuffle(shuffled_notes)
            note_sequence = ''.join(shuffled_notes)
            
            # Add to history
            self.add_to_history('location', note_sequence)
        
        
        current_exercise = self.history[self.history_index]
        self.clear_screen()
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}{current_exercise['content']}{Style.RESET_ALL}")
        self.show_navigation()
    
    def fret_to_note_exercise(self, from_history=False):
        """Generate fret positions on 6 strings with visualization"""
        if not from_history:
            # Generate random fret positions for each string (1-12 frets)
            fret_positions = [random.randint(1, 12) for _ in range(6)]
            string_fret_pairs = list(zip(self.strings, fret_positions))
            
            # Add to history
            self.add_to_history('inverse-location', string_fret_pairs)
        current_exercise = self.history[self.history_index]
        
        # Display the fretboard for each string
        self.clear_screen()
        for i, (string_name, fret_pos) in enumerate(current_exercise['content']):
            self.draw_string_fretboard(fret_pos, i+1)
        self.show_navigation()
    
    def draw_string_fretboard(self, target_fret, string_number):
        """Draw a single string's fretboard with highlighted position"""
        line = f"{string_number} "
        
        for fret in range(1, 13):  # 1-12 frets (skip open string)
            if fret == target_fret:
                # Highlighted fret position
                line += f"|{Fore.CYAN}{Style.BRIGHT} ● {Style.RESET_ALL}"
            elif fret in [3, 5, 7, 9]:
                # Position markers
                line += f"{Fore.WHITE}| • {Style.RESET_ALL}"
            elif fret == 12:
                # 12th fret marker
                line += f"{Fore.WHITE}| : {Style.RESET_ALL}"
            else:
                # Regular fret
                line += f"{Fore.WHITE}|   {Style.RESET_ALL}"
        
        line += "|"
        print(line)
    
    def generate_new_same_type(self):
        """Generate a new exercise of the same type as current"""
        if self.history_index >= 0 and self.history_index < len(self.history):
            current_exercise = self.history[self.history_index]
            if current_exercise['type'] == 'location':
                self.note_to_fret_exercise()
            else:  # inverse-location
                self.fret_to_note_exercise()
    
    def run(self):
        """Main application loop"""
        try:
            self.enter_alternate_screen()
            self.show_header()
            self.show_navigation()
            
            while True:
                key = self.get_single_key()
                
                if key.lower() == 'z':
                    self.note_to_fret_exercise()      
                elif key.lower() == 'x':
                    self.fret_to_note_exercise()
                elif key == ' ':  # Space key
                    self.generate_new_same_type()
                elif key.lower() == 'b' or key == '\033[D':  # B key or left arrow
                    if self.navigate_history(-1):
                        self.show_current_exercise()
                elif key.lower() == 'n' or key == '\033[C':  # N key or right arrow
                    if self.navigate_history(1):
                        self.show_current_exercise()         
                elif ord(key[0]) == 3:  # Ctrl+C
                    break
        
        except KeyboardInterrupt:
            pass
        finally:
            self.exit_alternate_screen()

def main():
    trainer = FretTrainer()
    trainer.run()

if __name__ == "__main__":
    main()