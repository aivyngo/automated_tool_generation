# tools/create_code_file.py

from pathlib import Path

def create_code_file(app_name, file_name, code):
    """
    Creates a file named 'file_name' under 'apps/app_name/' (checks if it exists, if it doesn't, makes it).
    The content inside the file is 'code'.
    The types of files that can be created are (loosely resembling these names):
    - 'main.py'
    - 'tool.py'
    - 'test.py'
    """
    base_dir = Path(__file__).parent
    app_dir = base_dir / "apps" / app_name
    app_dir.mkdir(parents=True, exist_ok=True)
    file_path = app_dir / file_name
    file_path.write_text(code)
    return str(file_path.resolve())