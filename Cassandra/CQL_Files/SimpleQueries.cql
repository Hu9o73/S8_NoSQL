-- List of Publications

SELECT * FROM publications;

-- List of publications titles

SELECT title FROM publications;

-- Booktitle of publications id "series/sci/2008-156"

SELECT booktitle FROM publications WHERE art_id = 'series/sci/2008-156';

-- Number of "Book" publications

SELECT COUNT(*) FROM publications WHERE type = 'Book';

-- Number of publications WHERE booktitle is equal to "HICSS"

SELECT COUNT(*) FROM publications WHERE booktitle = 'HICSS';

-- Use "ALLOW FILTERING" to execute the query

SELECT COUNT(*) FROM publications WHERE booktitle = 'HICSS' ALLOW FILTERING;

-- Create a secondary index on the "booktitle" attribute to be more efficient
-- Execute the query again without "ALLOW FILTERING"

CREATE INDEX publications_booktitle_idx ON publications(booktitle);

-- Number of publications where type is "Article" and booktitle is equal to "HICSS"

SELECT COUNT(*) FROM publications WHERE type = 'Article' AND booktitle = 'HICSS' ALLOW FILTERING;

-- Number of authors whose position is equal to 3

SELECT COUNT(*) FROM authors WHERE pos = 3 ALLOW FILTERING;

-- Number of authors whose position is above to 3

SELECT COUNT(*) FROM authors WHERE pos > 3 ALLOW FILTERING;
