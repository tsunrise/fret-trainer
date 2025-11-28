# Guitar Fret Trainer 🎸

A simple CLI tool for help you memorize guitar fret positions. 

I'm using it for my daily exercises and find it useful. 

## Requirements

- Python 3.8 or higher
- colorama

## Installation

Install from PyPI:

```bash
pip install fret-training
```

Or install from source:

```bash
pip install -e .
```

## Build

To build the package locally:

```bash
pip install build
python -m build
```

This will create distribution files in the `dist/` directory.

## Usage

Run the trainer:

```bash
fret-training
```

Or run directly:

```bash
python fret.py
```

### Controls

- **Z** - Note to Fret Exercise: Displays a randomly sorted string of seven notes (CDEFGAB)
- **X** - Fret to Note Exercise: Shows random fret positions on all six strings
- **Space** - Generate a new exercise of the same type
- **B** or **Left Arrow** - Go back in exercise history
- **N** or **Right Arrow** - Go forward in exercise history
- **Ctrl+C** - Exit the application
