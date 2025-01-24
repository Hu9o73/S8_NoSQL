# Script tested in python 3.9
# Doesn't work with python 3.11 or over

from cassandra.cluster import Cluster

def main():
    try:        
        print("Connecting to DB...")
        # Connect to Cassandra cluster
        cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra host
        session = cluster.connect('dblp')  # Connect to the DBLP keyspace

        # Step 1: Get all art_id's where Oscar Castillo is an author
        print("Getting the art_id of Oscar Castillo's publications...")
        query = "SELECT art_id FROM authors_publis WHERE author = 'Oscar Castillo'"
        rows = session.execute(query)

        print("Getting the co-authors...")
        author_list = []
        # Step 2: For each art_id, get the other authors who published with Oscar Castillo
        for row in rows:
            art_id = row.art_id
            query = f"SELECT author FROM authors_publis WHERE art_id = '{art_id}' ALLOW FILTERING"
            authors = session.execute(query)
            
            # Filter out 'Oscar Castillo' from the authors
            print(f"Authors for publication {art_id}:")
            for author in authors:
                if author.author != 'Oscar Castillo':  # Filter out Oscar Castillo
                    print(f"- {author.author}")
                    if author.author not in author_list:
                        author_list.append(author.author)
            print()

        # Close the session
        cluster.shutdown()

        print("The following authors are co-authors of Oscar Castillo:\n")
        for a in author_list:
            print(f"- {a}")

    except Exception as e:
        print(f"Error while querying : {e}")
    

if __name__ == '__main__':
    main()