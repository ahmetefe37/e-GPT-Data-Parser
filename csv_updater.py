#!/usr/bin/env python
import os
import argparse
from csv_converter import process_all_stages

def main():
    parser = argparse.ArgumentParser(description='Convert JSON files to CSV format across all stages')
    parser.add_argument('--json-dir', help='Path to JSON files directory (default: json-files)',
                      default=None)
    parser.add_argument('--csv-dir', help='Path to CSV files directory (default: csv-files)',
                      default=None)
    parser.add_argument('--max-stages', help='Maximum number of stages to process (default: 5)',
                      type=int, default=5)
    
    args = parser.parse_args()
    
    # Get base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use provided paths or defaults
    json_dir = args.json_dir or os.path.join(base_dir, 'json-files')
    csv_dir = args.csv_dir or os.path.join(base_dir, 'csv-files')
    
    # Verify JSON directory exists
    if not os.path.exists(json_dir):
        print(f"Error: JSON directory not found: {json_dir}")
        return
    
    print(f"Using directories:")
    print(f"JSON: {json_dir}")
    print(f"CSV: {csv_dir}")
    print(f"Maximum stages: {args.max_stages}")
    print("-" * 50)
    
    # Convert JSON files to CSV
    process_all_stages(json_dir, csv_dir, args.max_stages)

if __name__ == "__main__":
    main()
