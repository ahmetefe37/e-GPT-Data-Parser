import os
import json
import shutil

def read_file_content(file_path):
    """
    Read content of a file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

def get_base_filename(filename):
    """
    Get filename without extension
    """
    return os.path.splitext(filename)[0]

def get_instruction_content(instructions_dir, base_name):
    """
    Get instruction content for a circuit
    """
    instruction_file = os.path.join(instructions_dir, f"{base_name}.txt")
    if os.path.exists(instruction_file):
        content = read_file_content(instruction_file)
        if content:
            return content
    return "CIRCUIT EXAMPLE"  # Default instruction if file not found or empty

def get_circuit_pairs(schematics_dir, outputs_dir):
    """
    Get matched circuit pairs from directories
    """
    circuit_pairs = []
    schematic_files = {}
    output_files = {}
    
    # Get instructions directory path
    instructions_dir = os.path.join(os.path.dirname(schematics_dir), 'instructions')
    
    # Collect files from schematics directory
    for f in os.listdir(schematics_dir):
        if f.endswith(('.asc', '.plt')):
            base_name = get_base_filename(f)
            schematic_files[base_name] = f
    
    # Collect files from outputs directory
    for f in os.listdir(outputs_dir):
        if f.endswith(('.asc', '.plt')):
            base_name = get_base_filename(f)
            output_files[base_name] = f
    
    # Match files by name (regardless of extension)
    for base_name in schematic_files:
        if base_name in output_files:
            schematic_path = os.path.join(schematics_dir, schematic_files[base_name])
            output_path = os.path.join(outputs_dir, output_files[base_name])
            
            schematic_content = read_file_content(schematic_path)
            output_content = read_file_content(output_path)
            
            if schematic_content is not None and output_content is not None:
                # Get instruction content
                instruction_content = get_instruction_content(instructions_dir, base_name)
                
                example = {
                    "instruction": instruction_content,
                    "input": schematic_content,
                    "response": output_content
                }
                circuit_pairs.append(example)
                print(f"Matched files: {schematic_files[base_name]} <-> {output_files[base_name]} (Instruction: {instruction_content})")
    
    return circuit_pairs

def process_directories(schematics_dir, outputs_dir, output_json_path):
    """
    Process schematics and outputs directories to create Alpaca format JSON
    """
    json_data = get_circuit_pairs(schematics_dir, outputs_dir)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    # Save to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    print(f"Processed {len(json_data)} circuit pairs")

def rotate_backups(base_dir, max_stages=5):
    """
    Rotate backup files through stages
    """
    # Start from the highest stage and move down
    for stage in range(max_stages - 1, 0, -1):
        current_stage = os.path.join(base_dir, f'stage{stage}')
        next_stage = os.path.join(base_dir, f'stage{stage + 1}')
        
        # Create directories if they don't exist
        os.makedirs(current_stage, exist_ok=True)
        os.makedirs(next_stage, exist_ok=True)
        
        current_file = os.path.join(current_stage, 'converted_data.json')
        next_file = os.path.join(next_stage, 'converted_data.json')
        
        # If we're at the last stage, clear the directory first
        if stage == max_stages - 1 and os.path.exists(next_file):
            os.remove(next_file)
        
        # Move file if it exists
        if os.path.exists(current_file):
            shutil.copy2(current_file, next_file)

def update_json_data(schematics_dir, outputs_dir, json_dir):
    """
    Update JSON data and manage backups
    """
    stage1_path = os.path.join(json_dir, 'stage1', 'converted_data.json')
    
    # Get current and new circuit pairs
    new_pairs = get_circuit_pairs(schematics_dir, outputs_dir)
    current_pairs = []
    
    if os.path.exists(stage1_path):
        with open(stage1_path, 'r') as f:
            current_pairs = json.load(f)
    
    # Compare the number of pairs
    if len(new_pairs) != len(current_pairs):
        print(f"Changes detected: Current pairs: {len(current_pairs)}, New pairs: {len(new_pairs)}")
        
        # Rotate backups
        rotate_backups(json_dir)
        
        # Save new data
        os.makedirs(os.path.dirname(stage1_path), exist_ok=True)
        with open(stage1_path, 'w') as f:
            json.dump(new_pairs, f, indent=4)
        
        print("JSON data updated and backups rotated")
    else:
        print("No changes detected in circuit pairs")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schematics_dir = os.path.join(base_dir, "circuit-files", "schematics")
    outputs_dir = os.path.join(base_dir, "circuit-files", "outputs")
    json_dir = os.path.join(base_dir, "json-files")
    
    update_json_data(schematics_dir, outputs_dir, json_dir)