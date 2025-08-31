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

    def get_single_key(self):
        """Get a single key press without pressing Enter"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def show_welcome(self):
        print("\n" + "="*50)
        print("🎸 GUITAR FRET TRAINER 🎸")
        print("="*50)
        print("\nWelcome! This app helps you learn guitar fret positions.")
        print("\nInstructions:")
        print("• Press 'Z' for Location Exercise (identify notes)")
        print("• Press 'X' for Inverse-Location Exercise (fret positions)")
        print("• Press Ctrl+C to exit")
        print("\nReady to start? Press Z or X...")
    
    def location_exercise(self):
        """Generate random sequence of 7 unique notes"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        shuffled_notes = self.notes.copy()
        random.shuffle(shuffled_notes)
        
        note_sequence = ''.join(shuffled_notes)
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}{note_sequence}{Style.RESET_ALL}")
    
    def inverse_location_exercise(self):
        """Generate fret positions on 6 strings with visualization"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Generate random fret positions for each string (1-12 frets)
        fret_positions = [random.randint(1, 12) for _ in range(6)]
        
        # Display the fretboard for each string
        for i, (string_name, fret_pos) in enumerate(zip(self.strings, fret_positions)):
            self.draw_string_fretboard(string_name, fret_pos, i+1)
    
    def draw_string_fretboard(self, string_name, target_fret, string_number):
        """Draw a single string's fretboard with highlighted position"""
        line = f"{string_name} "
        
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
    
    def run(self):
        """Main application loop"""
        try:
            self.show_welcome()
            
            while True:
                key = self.get_single_key().lower()
                
                if key == 'z':
                    self.location_exercise()      
                elif key == 'x':
                    self.inverse_location_exercise()         
                elif ord(key) == 3:  # Ctrl+C
                    break
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Thanks for using Guitar Fret Trainer! Keep practicing! 🎸{Style.RESET_ALL}")
            sys.exit(0)

def main():
    trainer = FretTrainer()
    trainer.run()

if __name__ == "__main__":
    main()