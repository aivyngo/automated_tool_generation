# tools/stop_server.py

import psutil

def stop_server(pid: int) -> str:
    """
    Stops a server process by PID.
    """
    try:
        p = psutil.Process(pid)
        p.terminate()
        try:
            p.wait(timeout=3)
            return f"Stopped server with PID {pid}."
        except psutil.TimeoutExpired:
            p.kill()
            return f"Force killed server with PID {pid}."
    except psutil.NoSuchProcess:
        return f"No process found with PID {pid}."
    except Exception as e:
        return f"Unexpected error while stopping PID {pid}: {type(e).__name__} - {e}"