import json

from tool_interface import TOOL_DEFINITION, call_tool


# Display the tool definition.
print("=== Tool Definition ===")
print(json.dumps(TOOL_DEFINITION, indent=2))


# Simulate an Agent calling the tool.
print("\n=== Tool Execution ===")

result = call_tool(
    "analyze_automotive_log",
    {
        "file_path": "tools/log_parser/sample.csv"
    }
)

print(json.dumps(result, indent=2))


# Test an invalid tool name.
print("\n=== Invalid Tool Test ===")

error_result = call_tool(
    "unknown_tool",
    {}
)

print(json.dumps(error_result, indent=2))
