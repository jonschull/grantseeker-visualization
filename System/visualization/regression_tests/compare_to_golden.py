import difflib
import sys
from pathlib import Path

GOLDEN = Path(__file__).parent.parent / 'golden_master' / 'opportunity_visualization_golden.html'
OUTPUT = Path(__file__).parent.parent / 'outputs' / 'opportunity_visualization.html'

def read_lines(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)

def main():
    golden_lines = read_lines(GOLDEN)
    output_lines = read_lines(OUTPUT)
    diff = difflib.unified_diff(
        golden_lines, output_lines,
        fromfile=str(GOLDEN),
        tofile=str(OUTPUT),
        lineterm=''  # No extra newlines
    )
    diff_list = list(diff)
    if diff_list:
        print("Differences detected between Golden Master and current output:")
        for line in diff_list:
            print(line)
    else:
        print("No differences detected. Output matches Golden Master.")

if __name__ == "__main__":
    main()
