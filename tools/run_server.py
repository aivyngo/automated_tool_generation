# tools/run_server.py

import subprocess

def run_server(port, app_name):
    """
    Start FastAPI app 'app_name.main:app' on a given port.
    Uses subprocess so the agent can keep running.
    """
    cmd = [
        "uvicorn",
        f"tools.apps.{app_name}.main:app",
        "--host", "127.0.0.1",
        "--port", str(port),
        "--reload"
    ]
    process = subprocess.Popen(cmd)
    return process.pid