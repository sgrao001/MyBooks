#!/usr/bin/env python3
"""
find_missing_jpegs.py - Find JPEG files in a directory that are missing from a source file.

Usage: python find_missing_jpegs.py source_file
"""

import os
import sys
import argparse
import re

def get_jpeg_files(directory, recursive=False):
    """Get all .jpeg and .jpg files in the specified directory, optionally recursively."""
    jpeg_files = set()
    
    try:
        if recursive:
            # Walk through all subdirectories
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    if filename.lower().endswith(('.jpeg', '.jpg')):
                        # Store the relative path from the search directory
                        full_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(full_path, directory)
                        jpeg_files.add(rel_path)
        else:
            # Only search the specified directory
            for filename in os.listdir(directory):
                if filename.lower().endswith(('.jpeg', '.jpg')):
                    jpeg_files.add(filename)
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied to access directory '{directory}'.")
        sys.exit(1)
    
    return jpeg_files

def read_source_file(source_file_path):
    """Read the source file and extract all JPEG filenames mentioned in it."""
    # Updated pattern to include hyphens, underscores, spaces, ampersands, and other common filename characters
    jpeg_pattern = re.compile(r'\b([\w\s\.\-_&]+\.(?:jpe?g|JPE?G))\b')
    mentioned_files = set()
    
    try:
        with open(source_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            matches = jpeg_pattern.findall(content)
            mentioned_files = set(matches)
    except FileNotFoundError:
        print(f"Error: Source file '{source_file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading source file: {e}")
        sys.exit(1)
    
    return mentioned_files

def main():
    parser = argparse.ArgumentParser(
        description="Find JPEG files in a directory that are missing from a source file."
    )
    parser.add_argument(
        "source_file",
        help="Path to the source file to search for JPEG references"
    )
    parser.add_argument(
        "-d", "--directory",
        help="Directory to search for JPEG files (default: directory of source file)",
        default=None
    )
    parser.add_argument(
        "-r", "--recursive",
        help="Search for JPEG files recursively in subdirectories",
        action="store_true"
    )
    parser.add_argument(
        "-q", "--quiet",
        help="Quiet mode - only output the list of missing files",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Determine which directory to search
    if args.directory:
        search_dir = args.directory
    else:
        search_dir = os.path.dirname(args.source_file) or "."  # Current directory if empty
    
    # Get JPEG files from directory and source file
    directory_files = get_jpeg_files(search_dir, args.recursive)
    mentioned_files = read_source_file(args.source_file)
    
    if not args.quiet:
        print(f"Directory: {os.path.abspath(search_dir)}")
        print(f"Source file: {os.path.abspath(args.source_file)}")
        print(f"Found {len(directory_files)} JPEG files in directory")
        print(f"Found {len(mentioned_files)} JPEG references in source file")
        print("-" * 60)
    
    # Find files that exist in directory but are not mentioned in source file
    missing_files = directory_files - mentioned_files
    
    if missing_files:
        if not args.quiet:
            print(f"\n{len(missing_files)} JPEG files are MISSING from the source file:")
            print("-" * 40)
        for filename in sorted(missing_files):
            print(filename)
    elif not args.quiet:
        print("\n✓ All JPEG files in the directory are mentioned in the source file!")
    
    # Optional: Show files that are mentioned but don't exist (for completeness)
    nonexistent_files = mentioned_files - directory_files
    if nonexistent_files and not args.quiet:
        print(f"\n{len(nonexistent_files)} JPEG files are mentioned but DON'T EXIST in directory:")
        print("-" * 50)
        for filename in sorted(nonexistent_files):
            print(f"  {filename}")

if __name__ == "__main__":
    main()
    