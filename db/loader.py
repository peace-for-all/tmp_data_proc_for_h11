import traceback
import os
import sys
import argparse
import pandas as pd
from config import config
from connector import Connector


class Loader:
    def __init__(self, table_name, date):
        self.table_name = table_name
        self.date = date
        self.config = config.get(table_name, {})
        self.db_connector = Connector()

    def load(self):
        if not self.config:
            print(f"No config section for table: {self.table_name}")
            sys.exit(1)

        source_data_dir = self.config.get('source_data_dir')
        file_format = self.config.get('file_format')

        # Construct file path
        file_path = os.path.join(source_data_dir, f"{self.date}.{file_format}")

        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            sys.exit(1)

        df = pd.read_csv(file_path)

        engine = self.db_connector.get_engine()

        # Write data to MySQL table
        try:
            df.to_sql(self.table_name, con=engine, if_exists='append', index=False)
        except Exception as e:  # todo check we'll ever get here!
            print(f"Error loading data into table: {self.table_name}")
            print(traceback.format_exc())
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load data into table')
    parser.add_argument('--table-name', required=True)
    parser.add_argument('--date', required=True)
    args = parser.parse_args()

    loader = Loader(args.table_name, args.date)
    loader.load()
