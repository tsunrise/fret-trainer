# Guitar Fret Trainer 🎸

A simple CLI tool for help you memorize guitar fret positions. 

I'm using it for my daily exercises and find it useful. 

## Requirements

- Python 3.8 or higher
- colorama

## Installation

Install from PyPI:

```bash
pip install fret-trainer
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

## Release

To create a new release (bumps minor version):

```bash
python release.py
git push && git push --tags
```

This will:
1. Bump the minor version in `pyproject.toml` (e.g., 0.1.0 → 0.2.0)
2. Create a git commit with the version change
3. Create a git tag (e.g., `v0.2.0`)

The GitHub Actions workflow will automatically publish to PyPI when the tag is pushed.

## Usage

Run the trainer:

```bash
fret-trainer
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
