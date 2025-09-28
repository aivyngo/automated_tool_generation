# tools/revise_code_file.py

from pathlib import Path

def revise_code_file(app_name, file_name, code):
    """
    Revises a file named 'file_name' under 'apps/app_name/'.
    The content inside the file is 'code'.
    """
    base_dir = Path(__file__).parent 
    app_dir = base_dir / "apps" / app_name  
    app_dir.mkdir(parents=True, exist_ok=True)  
    file_path = app_dir / file_name        

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist. Use create_code_file first.")
    
    file_path.write_text(code)  
    return str(file_path.resolve())