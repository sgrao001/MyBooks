#!/usr/bin/env python3
import sys
import re

def count_words(line):
    """Count words in a line (split by whitespace)"""
    return len(line.split())

def process_file(filename, wordcountn):
    PageMarker = "\n![[]]<br>\n"
    
    """Process the file according to the specified rules"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    output_lines = []
    word_count = 0
    counting_enabled = False
    
    for line in lines:
        # Check if we encounter ![[ to start counting
        if "![[" in line:
            counting_enabled = True
            word_count = 0
            output_lines.append(line)
            continue
        
        # If counting is not enabled yet, just add the line
        if not counting_enabled:
            output_lines.append(line)
            continue
        
        # Check if this is a blank line
        if line.strip() == "":
            # If word count exceeds threshold, replace with --PB--
            if word_count > wordcountn:
                output_lines.append(PageMarker)
                word_count = 0
            else:
                output_lines.append(line)
            continue
        
        # Regular line - count words and add to output
        word_count += count_words(line)
        output_lines.append(line)
    
    # Write the processed content back to the file
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(output_lines)
        print(f"File '{filename}' processed successfully.")
    except Exception as e:
        print(f"Error writing file: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <wordcountn>")
        print("  filename:    The file to process")
        print("  wordcountn:  The word count threshold for inserting --PB--")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        wordcountn = int(sys.argv[2])
    except ValueError:
        print("Error: wordcountn must be an integer")
        sys.exit(1)
    
    process_file(filename, wordcountn)

if __name__ == "__main__":
    main()