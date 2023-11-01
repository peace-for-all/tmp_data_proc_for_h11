from dotenv import load_dotenv
import os
from sqlalchemy import create_engine


class Connector:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Extract MySQL connection info from environment variables
        self.host = os.getenv('MYSQL_HOST')
        self.port = os.getenv('MYSQL_PORT', 3306)  # Default port is 3306
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASS')

    def get_engine(self):
        # Construct MySQL connection URL
        url = f"mysql+mysqldb://{self.user}:{self.password}@{self.host}:{self.port}"

        # Create and return SQLAlchemy engine
        engine = create_engine(url, echo=True)
        return engine
