import pandas as pd
import json
import logging

def json_to_csv(json_file, csv_file):
    try:
        # Load the JSON data
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Convert the JSON data to a DataFrame
        df = pd.DataFrame(data)
        
        # Save the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)
        
        logging.info(f"Successfully converted {json_file} to {csv_file}")
    except FileNotFoundError:
        logging.error(f"File {json_file} not found.")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {json_file}.")
    except IOError as e:
        logging.error(f"IO error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    json_to_csv('data_output.json', 'data_output.csv')
