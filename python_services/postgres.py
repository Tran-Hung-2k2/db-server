import psycopg2
import csv

# PostgreSQL database connection parameters
db_params = {
    'dbname': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_2O8YFLTThEFiF075YFt',
    'host': 'pg-1ade2076-hoatungduong12-7d05.a.aivencloud.com',
    'port': '13340',
    'sslmode': 'require'
}

# CSV file path
csv_file = 'hungtv.csv'

def get_csv_header(csv_file):
    """Read the header of the CSV file to get column names."""
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Get the header row
    return header

def create_table(cursor, header):
    """Create a new table in the database based on CSV header."""
    column_definitions = ', '.join([f'{column_name} VARCHAR' for column_name in header])
    create_table_query = f"CREATE TABLE IF NOT EXISTS my_table ({column_definitions});"
    try:
        cursor.execute(create_table_query)
        print("Table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data(cursor, conn, csv_file):
    """Insert data from CSV file into the table."""
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            try:
                cursor.execute("INSERT INTO my_table VALUES (%s);" % ','.join(['%s'] * len(row)), row)
            except Exception as e:
                print(f"Error inserting row {row}: {e}")
    conn.commit()
    print("Data inserted successfully.")

def main():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Get CSV header to infer table schema
        header = get_csv_header(csv_file)

        # Create table dynamically based on CSV header
        create_table(cursor, header)

        # Insert data from CSV file
        insert_data(cursor, conn, csv_file)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close database connection
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
