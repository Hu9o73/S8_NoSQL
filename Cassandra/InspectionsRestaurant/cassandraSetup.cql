-- Creating the keyspace and using it

CREATE KEYSPACE IF NOT EXISTS InspectionsRestaurants
    WITH REPLICATION =
    {'class':'SimpleStrategy','replication_factor':3};

USE InspectionsRestaurants;

-- Table creation (Flattening the JSON's restaurant structure)

CREATE TABLE inspections (
    idRestaurant UUID PRIMARY KEY,
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

