import os
import json
from datetime import datetime
from tqdm import tqdm
import zipfile
import shutil


def collect_file_metadata(input_dir):
    """Collect file metadata, grouped by creation date."""
    metadata_by_date = {}
    
    # List all files in the input directory
    all_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    # Iterate through each file and collect its metadata
    for filepath in tqdm(all_files, desc="Processing files"):
        full_path = os.path.join(input_dir, filepath)
        
        # Extract creation date and use it as a key
        creation_timestamp = os.path.getctime(full_path)
        creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d')
        
        # File metadata
        metadata = {
            "filename": filepath,
            "path": full_path,
            "size": os.path.getsize(full_path),
            "creation_date": creation_date,
        }
        
        if creation_date not in metadata_by_date:
            metadata_by_date[creation_date] = []
        metadata_by_date[creation_date].append(metadata)
    
    return metadata_by_date


def save_metadata_to_json(metadata_by_date, tmp_dir):
    """Save collected metadata as JSON files."""
    for date, metadatas in tqdm(metadata_by_date.items(), desc="Writing JSON files"):
        json_file_path = os.path.join(tmp_dir, f"{date}.json")
        with open(json_file_path, 'w') as json_file:
            for metadata in metadatas:
                json.dump(metadata, json_file)
                json_file.write("\n")


def zip_tmp_dir(tmp_dir, output_file):
    """Compress the /tmp directory into a zip file."""
    with zipfile.ZipFile(output_file, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(tmp_dir):
            for filename in tqdm(filenames, desc="Zipping files"):
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, tmp_dir)
                zipf.write(file_path, arcname)


def main(input_dir, output_file):
    metadata_by_date = collect_file_metadata(input_dir)
    save_metadata_to_json(metadata_by_date, '/tmp')
    zip_tmp_dir('/tmp', output_file)
    shutil.rmtree('/tmp')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process input directory and save metadata to a .zip file.')
    parser.add_argument('input_dir', type=str, help='Path to the input directory.')
    parser.add_argument('output_file', type=str, help='Path to the output .zip file.')
    args = parser.parse_args()
    main(args.input_dir, args.output_file)
