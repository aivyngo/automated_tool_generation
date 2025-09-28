# tools/read_endpoint_code.py

from pathlib import Path

def read_endpoint_code(app_name, file_name):
    """
    Reads code of a particular endpoint.
    When we receive error signals, take the signals to call this tool
    to read the code of the endpoint to see what is wrong.
    """
    base_dir = Path(__file__).parent
    file_path = base_dir / "apps" / app_name / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    return file_path.read_text()