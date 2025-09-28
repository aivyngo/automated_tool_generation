# main.py
from tools.create_folder import create_folder
from tools.create_code_file import create_code_file
from tools.run_server import run_server
from tools.test_server import test_server
from tools.revise_code_file import revise_code_file
from tools.stop_server import stop_server
from tools.read_endpoint_code import read_endpoint_code
from tools.revise_endpoint import revise_endpoint
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()
app = FastAPI()

@app.get("/") 
def read_root():
    return {"message": "API is running."}

# ----CREATE FOLDER----
class CreateFolderInput(BaseModel):
    folder_name: str

@router.post("/create_folder")
def create_folder_endpoint(input_data: CreateFolderInput):
    folder_path = create_folder(input_data.folder_name)
    return { "message": "Folder successfully created.", "path": folder_path }

# ----CREATE CODE FILE----
class CreateCodeFileInput(BaseModel):
    app_name: str
    file_name: str
    code: str

@router.post("/create_code_file")
def create_code_file_endpoint(input_data: CreateCodeFileInput):
    file_path = create_code_file(input_data.app_name, input_data.file_name, input_data.code)
    return { "message": "File successfully created.", "path": file_path }

# ----RUN SERVER----
class RunServerInput(BaseModel):
    port: int 
    app_name: str
    
@router.post("/run_server")
def run_server_endpoint(input_data: RunServerInput):
    pid = run_server(input_data.port, input_data.app_name)
    return { "message": "Server running", "port": input_data.port, "pid": pid, "app": input_data.app_name }

# ----TEST SERVER----
class TestServerInput(BaseModel):
    port: int
    app_name: str
    api_name: str
    parameters: Dict 

@router.post("/test_server")
def test_server_endpoint(input_data: TestServerInput): 
    stdout, stderr, returncode = test_server(input_data.port, input_data.app_name, input_data.api_name, input_data.parameters)
    return {"success": returncode == 0,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": returncode}

@router.post("/test_server")
def test_server_endpoint(input_data: TestServerInput):
    result = test_server(input_data.port, input_data.app_name, input_data.api_name, input_data.parameters)
    return { "success": result.get("status", "ok") != "fail", "response": result }

# ----REVISE CODE FILE----
class ReviseCodeFileInput(BaseModel):
    app_name: str
    file_name: str
    code: str 
    
@router.post("/revise_code_file")
def revise_code_file_endpoint(input_data: ReviseCodeFileInput):
    file_path = revise_code_file(input_data.app_name, input_data.file_name, input_data.code)
    return { "message": "File successfully revised.", "path": file_path }

# ----STOP SERVER----
class StopServerInput(BaseModel):
    pid: int 

@router.post("/stop_server")
def stop_server_endpoint(input_data: StopServerInput):
    message = stop_server(int((input_data.pid)))
    return {"message": message}

# ----READ ENDPOINT CODE----
class ReadEndpointCodeInput(BaseModel):
    app_name: str
    file_name: str
    
@router.post("/read_endpoint_code")
def read_endpoint_code_endpoint(input_data: ReadEndpointCodeInput):
    code = read_endpoint_code(input_data.app_name, input_data.file_name)
    return {"code": code}

# ----REVISE ENDPOINT----
class ReviseEndpointInput(BaseModel):
    app_name: str
    file_name: str
    code: str

@router.post("/revise_endpoint")
def revise_endpoint_endpoint(input_data: ReviseEndpointInput):
    file_path = revise_endpoint(input_data.app_name, input_data.file_name, input_data.code)
    return { "message": "Endpoint successfully revised.", "path": file_path }

# ----UNIFY INTO ONE ENDPOINT CALL TOOL----
TOOLS = { "create_folder": create_folder,
         "create_code_file": create_code_file,
         "run_server": run_server,
         "test_server": test_server,
         "revise_code_file": revise_code_file,
         "stop_server": stop_server,
         "read_endpoint_code": read_endpoint_code,
         "revise_endpoint": revise_endpoint
         }

class CallToolInput(BaseModel):
    tool_name: str
    parameters: Dict[str, Any] 
    
@router.post("/call_tool")
def call_tool_endpoint(input_data: CallToolInput):
    func = TOOLS.get(input_data.tool_name)
    if not func:
        raise HTTPException(status_code=404, detail=f"Tool '{input_data.tool_name}' not found.")
    try: result = func(**input_data.parameters)
    except TypeError as e: raise HTTPException(status_code=400, detail = f"Invalid input for '{input_data.tool_name}': {e}")
    return {"tool_name": input_data.tool_name, "output": result}

app.include_router(router)