-- Creating the keyspace and using it

CREATE KEYSPACE IF NOT EXISTS DBLP
    WITH REPLICATION =
    {'class':'SimpleStrategy','replication_factor':3};

USE DBLP;

-- Creating tables

-- Publications

CREATE TABLE publications (
    art_id TEXT, type TEXT, title TEXT, pages_start INT, pages_end INT, booktitle TEXT,
    journal_series TEXT, journal_editor TEXT, journal_volume INT, journal_isbn TEXT,
    url TEXT, year INT,
    PRIMARY KEY(art_id)
);

ALTER TABLE publications WITH GC_GRACE_SECONDS=0;

CREATE INDEX btree_publi_type ON publications(type);

COPY publications(art_id, type, year, title, pages_start, pages_end, booktitle, journal_series,
    journal_editor, journal_volume, journal_isbn, url)
    FROM 'DBLP/DBLP_publis.csv' WITH HEADER = true AND DELIMITER=';';

-- Authors

CREATE TABLE authors (
    art_id TEXT, author TEXT, pos INT,
    PRIMARY KEY ((author), art_id)
);
ALTER TABLE authors WITH GC_GRACE_SECONDS = 0;
CREATE INDEX btree_authors_art_id on authors(art_id);
CREATE INDEX btree_authors_pos on authors(pos);
COPY authors(art_id,author,pos) FROM 'DBLP/authors.csv' WITH HEADER = true AND DELIMITER=';';

-- Author publications

CREATE TABLE authors_publis (
    art_id TEXT, author TEXT, type TEXT, title TEXT, pages_start FLOAT, pages_end FLOAT,
    booktitle TEXT, journal_series TEXT, journal_editor TEXT, journal_volume FLOAT,
    journal_isbn TEXT, url TEXT, year FLOAT, pos FLOAT,
    PRIMARY KEY ((author), art_id)
);
ALTER TABLE authors_publis WITH GC_GRACE_SECONDS = 0;
CREATE INDEX btree_authors_publi_type on authors_publis(type);
CREATE INDEX btree_authors_publi_title on authors_publis(title);
COPY authors_publis(art_id,author,type,year,title,pages_start,pages_end,booktitle,
    journal_series,journal_editor,journal_volume,journal_isbn,url,pos)
    FROM 'DBLP/authors_publis.csv' WITH HEADER = true AND DELIMITER=';';