import os
import glob
from data_loader import parse_single_xml


def process_folder(folder_path, file_pattern="*.xml"):
    xml_files = glob.glob(os.path.join(folder_path, file_pattern))
    
    if not xml_files:
        print(f"No XML files")
        return []
    
    all_data = []
    
    for xml_file in sorted(xml_files):
        filename = os.path.basename(xml_file)
        
        try:
            parsed_data = parse_single_xml(xml_file)
            parsed_data['filename'] = filename
            all_data.append(parsed_data)

            print(f"Glucose records: {len(parsed_data['glucose'])}")
            print(f"Meal records: {len(parsed_data['meals'])}")
            print(f"Bolus records: {len(parsed_data['bolus'])}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    return all_data

def process_training_testing_folders(data_folder="./data"):

    training_data = process_folder(data_folder, "*-training.xml")
    testing_data = process_folder(data_folder, "*-testing.xml")
    
    return {
        'training': training_data,
        'testing': testing_data
    }

if __name__ == "__main__":
        data = process_training_testing_folders(r".\data")