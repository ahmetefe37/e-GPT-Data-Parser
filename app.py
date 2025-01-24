import os
from json_converter import update_json_data
from csv_converter import process_all_stages

def main():
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schematics_dir = os.path.join(base_dir, 'circuit-files', 'schematics')
    outputs_dir = os.path.join(base_dir, 'circuit-files', 'outputs')
    json_dir = os.path.join(base_dir, 'json-files')
    csv_dir = os.path.join(base_dir, 'csv-files')
    
    print("=== Starting JSON Update Process ===")
    # Step 1: Update JSON data with backup management
    update_json_data(schematics_dir, outputs_dir, json_dir)
    
    print("\n=== Starting CSV Conversion Process ===")
    # Step 2: Convert JSON files to CSV format
    process_all_stages(json_dir, csv_dir)
    
    print("\n=== All processes completed ===")

if __name__ == "__main__":
    main()