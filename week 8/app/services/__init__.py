from pathlib import Path

# Create __init__.py files if they don't exist
Path("app/__init__.py").touch()
Path("app/data/__init__.py").touch()
Path("app/services/__init__.py").touch()
