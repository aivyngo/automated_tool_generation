# tools/create_folder.py

from pathlib import Path

def create_folder(folder_name):
    """
    Creates a folder for the new app inside 'apps/'.
    If 'apps' doesn't exist, it will be created automatically.
    Returns the full path of the created app folder.
    """
    base_dir = Path(__file__).parent
    parent = base_dir / "apps"
    
    parent.mkdir(exist_ok=True)
    
    app = parent / folder_name
    app.mkdir(exist_ok=True)

    return str(app.resolve())