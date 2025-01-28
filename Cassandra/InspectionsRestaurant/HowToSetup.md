## Run Cassandra

After Installing its image onto your computer, run Cassandra as a container using the command:

`docker run --rm -d --name Cassandra -p 127.0.0.1:9042:9042 cassandra`

### Side note: CQLSH debug

If encountering an 'Unable to connect to any server' when executing the `#cqlsh` command in the Exec section of your container, in your terminal run (Considering the container's name to be 'Cassandra'):

`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' Cassandra`

You'll then get the ip Cassandra is running on, you can then run (Considering the port to be set on 9042 as specified before):

`cqlsh <container_ip> 9042`

## Model the Table

Either using TablePlus or cqlsh from the exec panel of your container, create the keyspace and table that will hold your database. All the code can be found in `InspectionsRestaurant/cassandraSetup.cql` 

- Keyspace creation:

```
CREATE KEYSPACE restaurant_inspections WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};

USE restaurant_inspections;
```

- Table creation:

The table is created according to the model of the JSON file (check `Database/dataBatch.json`)

```
CREATE TABLE inspections (
    idRestaurant INT PRIMARY KEY,
    name TEXT,
    borough TEXT,
    buildingnum TEXT,
    street TEXT,
    zipcode TEXT,
    phone TEXT,
    cuisineType TEXT,
    inspectionDate DATE,
    violationCode TEXT,
    violationDescription TEXT,
    criticalFlag TEXT,
    score INT,
    grade TEXT
);
```

From this point you should be able to access the table 'inspections' from TablePlus or the cql shell.

## Insert Data

### Preparing the JSON

Cassandra's `COPY` command works with CSV files, so we first need to convert our JSON to CSV. We can use python to do so ! The script we'll run is in `Cassandra/InspectionsRestaurant/convert_json_to_csv.py`.

Modify the paths of `input_file` and `output_file` before running the script with the `python` command !

:warning: Our InspectionsRestaurant dataset has a ndjson format, not json. Thus, to avoid problems the python conversion function first converts the file to json before converting the json to csv. Direct conversion from NDJSON to CSV caused problems so that's how I overcame the issue !

You may want to skip the ndjson to json conversion if your file is already json.

### Loading into Cassandra

Once the `.csv` file is generated, we can use the cql shell to load the data into Cassandra. We shall move the .csv file to cassandra's container (if using docker) and run this command in the cql shell:

- Moving the .csv file to Cassandra's container:
    - We consider the container's name to be `Cassandra`
    - Run this in your powershell or host terminal

```
docker cp PATH_TO_FOLDER/your_file.csv Cassandra:/
```

- Copying the data from the CSV to the database:
    - Run this in the cqlsh
    
```
COPY inspections (idRestaurant, name, borough, buildingnum, street, zipcode, phone, cuisineType, inspectionDate, violationCode, violationDescription, criticalFlag, score, grade) 
FROM 'path/to/your_file.csv' 
WITH HEADER = TRUE;
```

We're using `WITH HEADER = TRUE` as our CSV has a header. 


