#!/usr/bin/env python3
"""
Release script to bump the minor version and create a git tag.

Usage:
    python release.py
"""

import re
import subprocess
import sys
from pathlib import Path


def get_current_version(pyproject_path: Path) -> str:
    """Read the current version from pyproject.toml."""
    content = pyproject_path.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def bump_minor_version(version: str) -> str:
    """Bump the minor version (e.g., 0.1.0 -> 0.2.0)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch = parts
    return f"{major}.{int(minor) + 1}.0"


def update_version_in_file(pyproject_path: Path, old_version: str, new_version: str) -> None:
    """Update the version in pyproject.toml using regex for precise matching."""
    content = pyproject_path.read_text()
    new_content = re.sub(
        rf'^(version\s*=\s*"){re.escape(old_version)}(")',
        rf"\g<1>{new_version}\g<2>",
        content,
        flags=re.MULTILINE,
    )
    pyproject_path.write_text(new_content)


def run_git_command(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command and optionally raise an error if it fails."""
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running git {' '.join(args)}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result


def check_working_directory_clean() -> bool:
    """Check if git working directory has uncommitted changes."""
    result = run_git_command(["status", "--porcelain"], check=False)
    return result.stdout.strip() == ""


def tag_exists(tag_name: str) -> bool:
    """Check if a git tag already exists."""
    result = run_git_command(["tag", "-l", tag_name], check=False)
    return tag_name in result.stdout.strip().split("\n")


def main() -> None:
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("Error: pyproject.toml not found", file=sys.stderr)
        sys.exit(1)

    # Check for uncommitted changes
    if not check_working_directory_clean():
        print("Error: Working directory has uncommitted changes. Please commit or stash them first.", file=sys.stderr)
        sys.exit(1)

    # Get current version and calculate new version
    current_version = get_current_version(pyproject_path)
    new_version = bump_minor_version(current_version)
    tag_name = f"v{new_version}"

    # Check if tag already exists
    if tag_exists(tag_name):
        print(f"Error: Tag {tag_name} already exists.", file=sys.stderr)
        sys.exit(1)

    print(f"Bumping version: {current_version} -> {new_version}")

    # Update pyproject.toml
    update_version_in_file(pyproject_path, current_version, new_version)
    print(f"Updated pyproject.toml")

    # Create git commit
    commit_message = f"Release {tag_name}"

    run_git_command(["add", "pyproject.toml"])
    run_git_command(["commit", "-m", commit_message])
    print(f"Created commit: {commit_message}")

    # Create git tag
    run_git_command(["tag", tag_name])
    print(f"Created tag: {tag_name}")

    print(f"\nRelease {tag_name} prepared successfully!")
    print(f"Run 'git push && git push --tags' to publish the release.")


if __name__ == "__main__":
    main()
