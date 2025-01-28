import json
import csv
import os

def main():
    # Input NDJSON file and output CSV file
    # By default, set to the dataBatch for testing purposes, can be changed to your actual (or full) dataset !
    input_file = '../../Database/dataBatch.ndjson'
    output_file = '../../Database/dataBatch.csv'

    # Turn the NDJSON file to a JSON file. (This step is needed if the input is an NDJSON file)
    converted_file = ndjson_to_json(input_file)

    # Open the JSON file and the CSV file
    with open(converted_file, 'r') as json_file, open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        # Parse the JSON array from the file
        records = json.load(json_file)

        # Define the field names for the CSV file
        fieldnames = [
            'idRestaurant', 'name', 'borough', 'buildingnum', 'street', 'zipcode', 'phone',
            'cuisineType', 'inspectionDate', 'violationCode', 'violationDescription', 
            'criticalFlag', 'score', 'grade'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Process each record in the JSON array
        total_records = len(records)
        for counter, record in enumerate(records, start=1):
            print(f'Processing... {round((counter / total_records) * 100, 2)}%')
            writer.writerow({
                'idRestaurant': record['idRestaurant'],
                'name': record['restaurant']['name'],
                'borough': record['restaurant']['borough'],
                'buildingnum': record['restaurant']['buildingnum'],
                'street': record['restaurant']['street'],
                'zipcode': record['restaurant']['zipcode'],
                'phone': record['restaurant']['phone'],
                'cuisineType': record['restaurant']['cuisineType'],
                'inspectionDate': record['inspectionDate'],
                'violationCode': record.get('violationCode', ''),
                'violationDescription': record.get('violationDescription', ''),
                'criticalFlag': record['criticalFlag'],
                'score': record['score'],
                'grade': record['grade']
            })

    print(f"Conversion complete! CSV file saved as '{output_file}'.")


def ndjson_to_json(ndjson_file):

    # Output JSON file
    json_file = os.path.splitext(ndjson_file)[0] + '.json'

    # Read the NDJSON file and convert to a JSON array
    data = []

    with open(ndjson_file, 'r') as infile:
        counter = 0
        for line in infile:
            counter += 1
            if line.strip():  # Skip empty lines
                try:
                    # Parse each line as a JSON object
                    record = json.loads(line)
                    data.append(record)
                    print(f"Processing... line {counter}")
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {line.strip()} - Error: {e}")
        
    # Write the JSON array to a file
    with open(json_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Converted NDJSON file '{ndjson_file}' to JSON file '{json_file}'.")

    return json_file


if __name__ == '__main__':
    main()
