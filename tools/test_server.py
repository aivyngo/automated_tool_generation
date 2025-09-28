# tools/test_server.py

# import subprocess
# import time, requests

# def test_server(port, app_name):
#     """
#     Runs the 'test.py' file of the 'app_name' on the port the app's server is running on.
#     Directory looks something like 'apps/app_name/test.py'.
#     Essentially running 'python3 test.py'.
#     """
#     def wait_for_server(port, timeout=5):
#         for _ in range(timeout * 2):  # check every 0.5s
#             try:
#                 r = requests.get(f"http://127.0.0.1:{port}/")
#                 if r.status_code == 200:
#                     return True
#             except requests.exceptions.ConnectionError:
#                 time.sleep(0.5)
#         return False
    
#     if not wait_for_server(port):
#         return "", f"Server on port {port} did not start in time.", 1
    
#     test_path = f"tools/apps/{app_name}/test.py"
#     result = subprocess.run(
#         ["python3", test_path],
#         capture_output=True,
#         text=True
#     )
#     return result.stdout, result.stderr, result.returncode

import requests

def test_server(port, app_name, api_name, parameters):
    """
    Test tool for a specific app and API.
    
    Args:
        port (int): Port the FastAPI server is running on.
        app_name (str): The app folder name under 'apps/'.
        api_name (str): The API file name (without .py).
        parameters (dict): The input parameters for the API's Pydantic model.
    
    Returns:
        dict: Response from the server (/mcp endpoint).
    """
    url = f"http://127.0.0.1:{port}/mcp"
    payload = {
        "tool_name": api_name,
        "parameters": parameters
    }
    
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"status": "fail", "message": str(e)}




