import os
from pathlib import Path

#Set the base directory 
BASE_DIR = Path('.')

# Create necessary directories if they don't exist.
# .mkdir(parents=True, exist_ok=True) creates directories safely without erroring
# exist_ok=True prevents an error if the directory already exists
Path("app").mkdir(exist_ok=True)
Path("app/data").mkdir(exist_ok=True)
Path("app/services").mkdir(exist_ok=True)

# .touch() creates an empty file. __init__.py files mark directories as Python packages
# module import from app.data import db
Path("app/__init__.py").touch(exist_ok=True)
Path("app/data/__init__.py").touch(exist_ok=True)
Path("app/services/__init__.py").touch(exist_ok=True)

print("✅ All package structure files (__init__.py) have been created successfully!")