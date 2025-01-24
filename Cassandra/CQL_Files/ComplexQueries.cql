-- Aggregates

-- Number of publications per author

SELECT author, COUNT(*) AS num_publications 
FROM authors 
GROUP BY author;

-- Number of publications per author when they are in third position

SELECT author, COUNT(*) AS num_publications 
FROM authors 
WHERE pos = 3 
GROUP BY author ALLOW FILTERING;        -- We add ALLOW FILTERING due to the "pos = 3"

-- Number of author per position (using pos as partition key)
    -- We create a new table where pos is part of the partition key:

CREATE TABLE authors_by_position (
    pos INT, author TEXT, art_id TEXT,
    PRIMARY KEY ((pos), author, art_id)
);

    -- Insert data using the insert_authors_by_pos.py file !
    -- May want to use COPY from author.csv to go wayyyyy faster !

    -- Query author per position

SELECT pos, COUNT(author) AS num_authors 
FROM authors_by_position 
GROUP BY pos;

-- Distribution of positions for "Oscar Castillo"

SELECT pos, COUNT(*) AS num_publications 
FROM authors_by_position 
WHERE author = 'Oscar Castillo' 
GROUP BY pos 
ALLOW FILTERING;



-- Joins and Denormalization

-- Give authors names for publications which title is "Medical imaging archiving: ...". 
-- Join between tables publications and authors

SELECT art_id FROM publications WHERE title = 'Medical imaging archiving: A comparison between several NoSQL solutions.' ALLOW FILTERING; 
    -- We use the result of the previous query to get the author
SELECT author FROM authors WHERE art_id = 'conf/bhi/SilvaBCO14';


-- Same query on the denormalized authors_publis table

SELECT author FROM authors_publis WHERE title = 'Medical imaging archiving: A comparison between several NoSQL solutions.';

-- Give titles and positions of publications from Oscar Castillo

SELECT title, pos FROM authors_publis WHERE author = 'Oscar Castillo';

-- Give authors names who published with Oscar Castillo

    -- Run the Oscar_Castillo_Complex_Query.py file


-- Denormalization with SET MAP LIST ...
    -- Create a JSON Standard

CREATE TYPE IF NOT EXISTS journalType (series TEXT, editor TEXT, volume INT, isbn SET<TEXT>);

CREATE TABLE publicationsNorm (
    id TEXT PRIMARY KEY,
    type TEXT,
    year INT,
    title TEXT,
    authors LIST<TEXT>,
    pages MAP<TEXT, INT>,
    booktitle TEXT,
    journal FROZEN<journalType>,
    url TEXT,
    cites SET<TEXT>
);

ALTER TABLE publicationsNorm WITH GC_GRACE_SECONDS = 0;


    -- Import test sample

INSERT INTO publicationsNorm JSON
'{
    "id": "series/cogtech/BrandhermSNL13", 
    "type": "Article", 
    "year": 2013,
    "title": "A SemProM Use Case: Health Care and Compliance.",
    "authors": ["Boris Brandherm", "Michael Schmitz", "Robert Ne?elrath", "Frank Lehmann"],
    "pages": {"start": 349, "end": 361}, 
    "booktitle": "SemProM",
    "journal": {"series": "", "editor": "", "volume": "0", "isbn": [""]},
    "url": "db/series/cogtech/364237376.html#BrandhermSNL13",
    "cites": [""]
}';

    -- Import data... (in docker CLI)
SOURCE '/DBLP.json';

-- Create an index on attribute title of new table

CREATE INDEX publicationsNorm_title_idx ON publicationsNorm(title);

-- Give authors names for publication Data Quality

SELECT authors FROM publicationsNorm WHERE title = 'Data Quality';

-- Give the journal's series of this publication in publicationsNorm

SELECT journal.series FROM publicationsNorm WHERE title = 'Data Quality';

