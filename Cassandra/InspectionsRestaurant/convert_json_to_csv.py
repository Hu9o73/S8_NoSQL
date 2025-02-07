import json
import csv
import os
import pandas as pd
import uuid

def main():
    # Input NDJSON file and output CSV file
    # By default, set to the dataBatch for testing purposes, can be changed to your actual (or full) dataset !
    input_file = '../../Bigdata/InspectionsRestaurant.json'
    output_file = '../../Bigdata/InspectionsRestaurant.csv'
    output_folder = '../../Bigdata/'

    # Turn the NDJSON file to a JSON file. (This step is needed if the input is an NDJSON file)
    #converted_file = ndjson_to_json(input_file)
    converted_file = input_file

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


    # Load CSV file
    df = pd.read_csv(output_file)

    # Define column subsets
    inspections_columns = ["idRestaurant", "inspectionDate", "violationCode", "violationDescription", "criticalFlag", "score", "grade"]
    restaurant_columns = ["idRestaurant", "name", "borough", "buildingnum", "street", "zipcode", "phone", "cuisineType"]

    # Extract tables
    inspections = df[inspections_columns].copy()
    restaurants = df[restaurant_columns].copy()

    # Generate UUIDs for each inspection row
    inspections["idInspection"] = [uuid.uuid4() for _ in range(len(inspections))]

    # Save to new CSV files
    inspections.to_csv(f"{output_folder}inspections.csv", index=False)
    restaurants.to_csv(f"{output_folder}restaurants.csv", index=False)

    inspections_restaurants_columns = ['idRestaurant', 'name', 'borough', 'inspectionDate', 'grade']
    inspections_restaurants = df[inspections_restaurants_columns]
    inspections_restaurants.to_csv(f"{output_folder}inspections_restaurants.csv", index=False)

    print("Files saved.")

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
