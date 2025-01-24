#!/usr/bin/env python
import os
import argparse
from json_converter import update_json_data

def main():
    parser = argparse.ArgumentParser(description='Update JSON data from circuit files with backup management')
    parser.add_argument('--schematics', help='Path to schematics directory (default: circuit-files/schematics)',
                      default=None)
    parser.add_argument('--outputs', help='Path to outputs directory (default: circuit-files/outputs)',
                      default=None)
    parser.add_argument('--json-dir', help='Path to JSON files directory (default: json-files)',
                      default=None)
    
    args = parser.parse_args()
    
    # Get base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use provided paths or defaults
    schematics_dir = args.schematics or os.path.join(base_dir, 'circuit-files', 'schematics')
    outputs_dir = args.outputs or os.path.join(base_dir, 'circuit-files', 'outputs')
    json_dir = args.json_dir or os.path.join(base_dir, 'json-files')
    
    # Verify directories exist
    for dir_path in [schematics_dir, outputs_dir]:
        if not os.path.exists(dir_path):
            print(f"Error: Directory not found: {dir_path}")
            return
    
    print(f"Using directories:")
    print(f"Schematics: {schematics_dir}")
    print(f"Outputs: {outputs_dir}")
    print(f"JSON: {json_dir}")
    print("-" * 50)
    
    # Update JSON data
    update_json_data(schematics_dir, outputs_dir, json_dir)

if __name__ == "__main__":
    main()
