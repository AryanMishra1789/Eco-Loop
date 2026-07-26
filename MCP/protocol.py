from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------
# Tool Definition
# ---------------------------------------------------------

@dataclass
class ToolDefinition:

    name: str

    description: str

    input_schema: Dict[str, Any]


# ---------------------------------------------------------
# Tool Call
# ---------------------------------------------------------

@dataclass
class ToolCall:

    id: str

    tool: str

    arguments: Dict[str, Any]


# ---------------------------------------------------------
# Tool Result
# ---------------------------------------------------------

@dataclass
class ToolResult:

    id: str

    success: bool

    result: Any = None

    error: Optional[str] = None


# ---------------------------------------------------------
# MCP Request
# ---------------------------------------------------------

@dataclass
class MCPRequest:

    request_id: str

    tool_calls: List[ToolCall]


# ---------------------------------------------------------
# MCP Response
# ---------------------------------------------------------

@dataclass
class MCPResponse:

    request_id: str

    results: List[ToolResult] = field(default_factory=list)