 # agent.py
from dotenv import load_dotenv
import os, requests, json, random
from openai import OpenAI
from pathlib import Path

load_dotenv()
API_KEY = os.environ.get("SUBCONSCIOUS_API_KEY")
client = OpenAI( base_url="https://api.subconscious.dev/v1", api_key=API_KEY )
tools = [
    {
        "type": "function",
        "name": "create_folder",
        "description": (
            "Creates a folder called 'folder_name' in 'apps/'. "
            "If a folder with the same name already exists, it is not created. "
            "If 'apps/' doesn't exist yet, it creates 'apps/'."
        ),
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 10,
        "parameters": {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "The name of the folder to be created."
                }
            },
            "required": ["folder_name"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "create_code_file",
        "description": (
            "Creates a file called 'file_name' under 'apps/app_name/'. "
            "If 'apps/app_name' doesn't exist yet, it creates it. "
            "The content inside the file is 'code'."
        ),
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 10,
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the app the file is being created for."
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file."
                },
                "code": {
                    "type": "string",
                    "description": "The code inside the file."
                }
            },
            "required": ["app_name", "file_name", "code"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "run_server",
        "description": "Runs 'app_name' FastAPI server on the given port.",
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 20,
        "parameters": {
            "type": "object",
            "properties": {
                "port": {
                    "type": "integer",
                    "description": "The port to run the server on."
                },
                "app_name": {
                    "type": "string",
                    "description": "The name of the app to run the server for."
                }
            },
            "required": ["port", "app_name"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "test_server",
        "description": "Tests a given API in the 'mcp' POST endpoint of an app's 'main.py'.",
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 20,
        "parameters": {
            "type": "object",
            "properties": {
                "port": {
                    "type": "integer",
                    "description": "Port that 'app_name''s server is running on."
                },
                "app_name": {
                    "type": "string",
                    "description": "The app that is being tested via its test file."
                },
                "api_name": {
                    "type": "string",
                    "description": "The name of the API being tested."
                },
                "parameters": {
                    "type": "dict",
                    "description": "The input parameters for the API's Pydantic model."
                }
            },
            "required": ["port", "app_name", "api_name", "parameters"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "revise_code_file",
        "description": "Revises code in a file by replacing old code in 'file_name' with 'code'.",
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 10,
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the app that has its file being revised."
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file that is being revised."
                },
                "code": {
                    "type": "string",
                    "description": "The code that goes in the file."
                }
            },
            "required": ["app_name", "file_name", "code"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "stop_server",
        "description": "Stops a running FastAPI server given its port ID, 'pid'.",
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 10,
        "parameters": {
            "type": "object",
            "properties": {
                "pid": {
                    "type": "integer",
                    "description": "The port ID of the server being stopped."
                }
            },
            "required": ["pid"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "read_endpoint_code",
        "description": "Reads the code inside an endpoint's file.",
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 10,
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the app the endpoint belongs to."
                },
                "file_name": {
                    "type": "string",
                    "description": "The file name of the endpoint."
                }
            },
            "required": ["app_name", "file_name"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "revise_endpoint_code",
        "description": "Revises an endpoint's code in a file by replacing old code in 'file_name' with 'code'.",
        "url": "http://192.222.54.121:8000/call_tool",
        "method": "POST",
        "timeout": 10,
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the app that has its file being revised."
                },
                "file_name": {
                    "type": "string",
                    "description": "The name of the file for the endpoint that is being revised."
                },
                "code": {
                    "type": "string",
                    "description": "The code that goes in the file."
                }
            },
            "required": ["app_name", "file_name", "code"],
            "additionalProperties": False
        }
    }
]

# Load all apps
from pathlib import Path
import json, random

all_apps_path = Path("all_apps.json")

with open(all_apps_path, "r", encoding="utf-8") as f:
    all_apps = json.load(f)

test_app = random.choice(all_apps)
print(f"Selected app: {test_app['app_name']}")

# Pretty print JSON for debugging
test_app = json.dumps(test_app, indent=2)

# instruct best way to generate test files into this main prompt
prompt = f""" You are given a JSON representation of an app:
json
    {test_app}
    that includes its name, its tools, each tool’s APIs, and descriptions of all the categories just mentioned.  
    You will generate a working FastAPI server for the given app where each API is represented as a Python file.  
    Use the descriptions of each category to make the FastAPI server working, functional, and consistent with the app context.  

    Each app will get its own folder under a general folder called `apps`.  
    In each app folder, there should be:
    - a `main.py` FastAPI app with a post endpoint called '/mcp'. This endpoint should:
        - import all functions of all the app's APIs
        - check the tool name
        - translate the parameters to an API's input class (Pydantic model)
        - call API_function(API input model)
        - return to client
        Here is an example of what the '\mcp' endpoint might look like:
        # Unified MCP endpoint
    @app.post("/mcp")
    async def mcp_endpoint(request: MCPRequest, background_tasks: BackgroundTasks):
        try:
            tool_name = request.tool_name
            parameters = request.parameters
            
            # Session management tools
            if tool_name == "create_browser_session":
                create_req = CreateSessionRequest(**parameters)
                return await create_session(create_req)
            
            elif tool_name == "list_browser_sessions":
                return await list_sessions()
            
            elif tool_name == "close_browser_session":
                close_req = CloseSessionRequest(**parameters)
                return await close_session(close_req)
            
            # Browser navigation tools
            elif tool_name == "browser_navigate":
                nav_req = BrowserNavigateRequest(**parameters)
                return await browser_navigate(nav_req)
            
            elif tool_name == "browser_click":
                click_req = BrowserClickRequest(**parameters)
                return await browser_click(click_req)
            
            elif tool_name == "browser_type":
                type_req = BrowserTypeRequest(**parameters)
                return await browser_type(type_req)
            
            elif tool_name == "browser_key":
                key_req = BrowserKeyRequest(**parameters)
                return await browser_key(key_req)
            
            elif tool_name == "browser_scroll":
                scroll_req = BrowserScrollRequest(**parameters)
                return await browser_scroll(scroll_req)
            
            elif tool_name == "browser_get_state":
                state_req = BrowserStateRequest(**parameters)
                return await get_browser_state(state_req)
            
            # Content extraction tool
            elif tool_name == "browser_extract_content":
                extract_req = BrowserExtractContentRequest(**parameters)
                return await browser_extract_content(extract_req)
            
            # Browser navigation tools
            elif tool_name == "browser_go_back":
                back_req = BrowserGoBackRequest(**parameters)
                return await browser_go_back(back_req)
            
            # Tab management tools
            elif tool_name == "browser_list_tabs":
                list_tabs_req = BrowserListTabsRequest(**parameters)
                return await browser_list_tabs(list_tabs_req)
            
            elif tool_name == "browser_switch_tab":
                switch_req = BrowserSwitchTabRequest(**parameters)
                return await browser_switch_tab(switch_req)
            
            elif tool_name == "browser_close_tab":
                close_tab_req = BrowserCloseTabRequest(**parameters)
                return await browser_close_tab(close_tab_req)
            
            # Agent tools
            elif tool_name == "browse_agent":
                agent_req = AgentTaskRequest(**parameters)
                return await run_agent_task(agent_req, background_tasks)
            
            elif tool_name == "retry_browse_agent":
                retry_req = RetryWithAgentRequest(**parameters)
                return await retry_with_browser_use_agent(retry_req, background_tasks)
            
            elif tool_name == "get_agent_task_status":
                task_id = parameters.get("task_id")
                if not task_id:
                    raise HTTPException(status_code=400, detail="task_id parameter required")
                return await get_agent_task_status(task_id)
            
            elif tool_name == "select_dropdown_option":
                select_req = SelectDropdownRequest(**parameters)
                return await select_dropdown_option(select_req)

            # Account management tools
            elif tool_name == "generate_account_credentials":
                cred_req = PasswordGenerationRequest(**parameters)
                return await generate_account_credentials(cred_req)
            
            elif tool_name == "retrieve_account_credentials":
                retrieve_req = AccountRetrievalRequest(**parameters)
                return await retrieve_account_credentials(retrieve_req)
            
            else:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {{tool_name}}")
                
        except Exception as e:
            logger.error(f"Error in MCP endpoint for tool {{request.tool_name}}: {{e}}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))

    - a separate file for each endpoint containing its logic, called 'api_name'.py, containing
    Pydantic models and a function for this endpoint.
    - testing is done using the test_server tool, which calls the /mcp endpoint of the running app for each API.

    Ensure that:
    - `main.py` imports all functions and includes them '/mcp'.
    - Each API import imports the necessary Pydantic models, and functions.  
    - `test.py` uses `requests` to send requests to the server endpoints and validates responses.  
    - The code is runnable without manual fixes.  
    - Do not use port 8000 for generated code and servers. 

    Follow this workflow  
    <reasoning>
        <subtask "set up folders">
        1. Create a folder for the given app under `apps`.
        <tool_call> use `create_folder` to create the necessary folders </tool_call>
        </subtask>
        <subtask "generate FastAPI code files">
            1. Generate `main.py` that creates a FastAPI app, includes all API functions as imports
            and creates POST endpoint called '\mcp' that checks tool name, translates parameters to an API's input class
            (a Pydantic model), calls the API function, and returns to client, and defines `if __name__ == "__main__": uvicorn.run(...)`. 
            In `main.py`, after creating the FastAPI app, make sure to import every API file's function and include it in the '\mcp' endpoint.
            Do not skip this. In `main.py`, always include `import uvicorn`.
            2. Generate one file per endpoint implementing its function logic and Pydantic models.  
            3. Generate `test.py` that imports `requests`, calls each endpoint, and checks responses.  
            <tool_call> use `create_code_file` to write each file </tool_call>
        </subtask>
        <subtask "run the FastAPI server">
            <tool_call> use `run_server` with the chosen port and app name </tool_call>
        </subtask>
        <subtask "test the FastAPI server">
            For each API, call the new `test_server` tool to test it individually.  
            The `test_server` tool should:
                - Take as input: port, app_name, api_name, and parameters for that API.  
                - Send a request to the app’s running FastAPI server (`/mcp` endpoint).  
                - Return the server’s JSON response (`status`, `result` or `fail`).  
            <tool_call> use `test_server` with (port, app_name, api_name, parameters) to test one API at a time </tool_call>
        </subtask>
        <subtask "revise code if needed">
            If any tests fail or imports are missing, update the corresponding file until all tests pass.  
            <tool_call> use `read_endpoint_code` to read failing code files </tool_call>
            <tool_call> use `revise_code_file` and `revise_endpoints` to fix failing code </tool_call>
        </subtask>
        <subtask "stop the server">
            <tool_call> use `stop_server` to stop the running FastAPI server </tool_call>
        </subtask>
    </reasoning>
    <complete>
    Report that the FastAPI app was successfully created, tested, and is fully functional.
    </complete>
    """

messages = [{"role": "user", "content": prompt}]

print("Starting generation.")

while True:
    response = client.chat.completions.create(
        model="tim-large",
        messages=messages,
        tools=tools
    )
    message = response.choices[0].message
    messages.append(message)

    if message.content and "<complete>" in message.content:
        print(message.content)
        break

    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            print(f"\n[TOOL CALL] {tool_name}")
            tool_def = next(t for t in tools if t["name"] == tool_call.function.name)
            result = requests.post(
                tool_def["url"],
                json={
                    "tool_name": tool_call.function.name,
                    "parameters": json.loads(tool_call.function.arguments)
                }
            ).json()

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })