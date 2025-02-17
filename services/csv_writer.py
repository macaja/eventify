import csv
import os

def output_to_csv(track_data, filename):
    """
    Outputs the track data to a CSV file in the 'data' folder.
    """
    output_folder = 'model_data'
    # Ensure the 'data' folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Define the full file path
    file_path = os.path.join(output_folder, filename)
    
    # Write the track data to the CSV file
    keys = track_data[0].keys()
    with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(track_data)
    
    print(f"Data successfully written to {file_path}")
