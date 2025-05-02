class DataLoader:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def load_data_from_csv(self, csv_file_path):
        import csv
        
        with open(csv_file_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)  # Get the headers from the first row

            # Create a table based on the CSV headers
            columns = ', '.join([f"{header} TEXT" for header in headers])
            create_table_query = f"CREATE TABLE IF NOT EXISTS data ({columns});"
            self.db_connection.execute(create_table_query)

            # Insert data into the table
            for row in csv_reader:
                placeholders = ', '.join(['?' for _ in row])
                insert_query = f"INSERT INTO data VALUES ({placeholders});"
                self.db_connection.execute(insert_query, row)

        self.db_connection.commit()