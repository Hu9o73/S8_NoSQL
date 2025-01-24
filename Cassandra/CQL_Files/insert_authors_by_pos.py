# Script tested in python 3.9
# Doesn't work with python 3.11 or over

from cassandra.cluster import Cluster

def main():
    try:
        # Connect to the Cassandra cluster
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('dblp')  # Use your keyspace name

        print("Successfully connected to DB")

        # Fetch data from the 'authors' table
        rows = session.execute('SELECT pos, author, art_id FROM authors')

        print(f"Got the rows from authors\nRow0 example :\n{rows[0]}\n")

        counter = 0

        # Insert data into 'authors_by_position' table
        for row in rows:
            counter +=1
            if(counter%100 == 0):
                print(f"Inserted {counter} rows...")
            session.execute(
                """
                INSERT INTO authors_by_position (pos, author, art_id)
                VALUES (%s, %s, %s)
                """,
                (row.pos, row.author, row.art_id)
            )

        print("Data transfer complete.")
    except Exception as e:
        print(f"Error while transfering data: {e}")
    

if __name__ == '__main__':
    main()