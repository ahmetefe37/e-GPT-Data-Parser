import os
import json
import csv
import shutil
import codecs

def clean_content(content):
    """
    Clean and prepare content for CSV
    - Replace newlines with space
    - Remove any existing quotes or delimiters that might interfere
    """
    if isinstance(content, str):
        # Replace newlines with spaces
        content = ' '.join(content.splitlines())
        # Remove any quotes that might interfere with CSV format
        content = content.replace('"', "'")
    return content

def convert_json_to_csv(json_file_path, csv_file_path):
    """
    Convert a JSON file to CSV format
    """
    try:
        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Clean and prepare data
        cleaned_data = []
        for item in data:
            cleaned_item = {
                'instruction': clean_content(item.get('instruction', '')),
                'input': clean_content(item.get('input', '')),
                'response': clean_content(item.get('response', ''))
            }
            cleaned_data.append(cleaned_item)
        
        # Write to CSV file with BOM for Excel
        with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, 
                                  fieldnames=['instruction', 'input', 'response'],
                                  delimiter=',',
                                  quoting=csv.QUOTE_ALL)  # Quote all fields
            writer.writeheader()
            writer.writerows(cleaned_data)
            
        print(f"Successfully converted {json_file_path} to {csv_file_path}")
        return True
    except Exception as e:
        print(f"Error converting {json_file_path}: {str(e)}")
        return False

def process_stage(json_dir, csv_dir, stage_num):
    """
    Process a single stage directory
    """
    json_stage_dir = os.path.join(json_dir, f'stage{stage_num}')
    csv_stage_dir = os.path.join(csv_dir, f'stage{stage_num}')
    
    # Skip if JSON stage directory doesn't exist
    if not os.path.exists(json_stage_dir):
        return False
    
    # Create CSV stage directory
    os.makedirs(csv_stage_dir, exist_ok=True)
    
    # Convert JSON file if it exists
    json_file = os.path.join(json_stage_dir, 'converted_data.json')
    if os.path.exists(json_file):
        csv_file = os.path.join(csv_stage_dir, 'converted_data.csv')
        return convert_json_to_csv(json_file, csv_file)
    
    return False

def process_all_stages(json_dir, csv_dir, max_stages=5):
    """
    Process all stage directories
    """
    success_count = 0
    
    # Process each stage
    for stage in range(1, max_stages + 1):
        if process_stage(json_dir, csv_dir, stage):
            success_count += 1
    
    print(f"Processed {success_count} stages successfully")
    return success_count

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(base_dir, "json-files")
    csv_dir = os.path.join(base_dir, "csv-files")
    
    process_all_stages(json_dir, csv_dir)