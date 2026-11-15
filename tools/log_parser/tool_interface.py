from log_parser import analyze_log, LogParseError


# 1. Tool definition: describe the tool to an Agent.
TOOL_DEFINITION = {
    "name": "analyze_automotive_log",
    "description": (
        "Analyze an automotive CAN CSV log. "
        "Calculate frame counts and inter-frame intervals by CAN ID."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the CAN CSV log file."
            }
        },
        "required": ["file_path"],
        "additionalProperties": False
    }
}


# 2. Tool execution: connect the tool to the actual Python API.
def execute_analyze_log(arguments):
    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": {
                "type": "InvalidArguments",
                "message": "Arguments must be a dictionary."
            }
        }

    if set(arguments.keys()) != {"file_path"}:
        return {
            "success": False,
            "error": {
                "type": "InvalidArguments",
                "message": "Exactly one argument is required: file_path."
            }
        }

    file_path = arguments["file_path"]

    if not isinstance(file_path, str) or not file_path.strip():
        return {
            "success": False,
            "error": {
                "type": "InvalidArguments",
                "message": "file_path must be a non-empty string."
            }
        }

    try:
        result = analyze_log(file_path)

        return {
            "success": True,
            "result": result
        }

    except (FileNotFoundError, LogParseError, OSError) as error:
        return {
            "success": False,
            "error": {
                "type": type(error).__name__,
                "message": str(error)
            }
        }


# 3. Tool dispatcher: select and execute a tool by name.
def call_tool(name, arguments):
    if name == TOOL_DEFINITION["name"]:
        return execute_analyze_log(arguments)

    return {
        "success": False,
        "error": {
            "type": "ToolNotFound",
            "message": f"Unknown tool: {name}"
        }
    }
