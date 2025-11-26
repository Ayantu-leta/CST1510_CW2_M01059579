import sqlite3
from pathlib import Path

# Path(__file__).parent gets the directory of the current script
# and also .parent.parent moves up two levels to the project root
ROOT_DIR = Path(__file__).parent.parent.parent

# Defines the path to the main data directory
DATA_DIR = ROOT_DIR / "DATA"

#Defines the full path for the SQLite database file inside the DATA directory
DB_PATH = DATA_DIR / "intelligence_platform.db"

#Defines the full paths for the three CSV files used for data loading
#The '/' operator provides platform-independent path joining
CYBER_INCIDENTS_CSV = DATA_DIR / "cyber_operations_incidents.csv"
DATASETS_METADATA_CSV = DATA_DIR / "datasets_metadata.csv"
IT_TICKETS_CSV = DATA_DIR / "it_tickets.csv"

def connect_database(db_path=DB_PATH):
    """
    Connects to the SQLite database. Creates the parent directory if it doesn't exist.
    
    Args:
        db_path (Path): The Path object pointing to the database file.
    
    Returns:
        sqlite3.Connection: An active connection object.
    """
    # to make sure the DATA directory exists before trying to create the database file in it
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # sqlite3.connect requires a string path so the Path object is converted using str()
    return sqlite3.connect(str(db_path))