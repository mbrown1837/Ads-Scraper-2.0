import json
import logging

class DataSaver:

    @staticmethod
    def save_data(data, output_file="data_output.json"):
        try:
            # Read existing data from the file
            with open(output_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, start with an empty list
            logging.warning(f"{output_file} not found. Creating a new file.")
            existing_data = []
        except json.JSONDecodeError:
            # If the file contains invalid JSON, start with an empty list
            logging.error(f"Error decoding JSON from {output_file}. Starting with an empty list.")
            existing_data = []
        except IOError as e:
            logging.error(f"IO error occurred while reading {output_file}: {e}")
            return

        # Append the new data
        existing_data.extend(data)

        # Write the updated data back to the file
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            logging.error(f"IO error occurred while writing to {output_file}: {e}")
