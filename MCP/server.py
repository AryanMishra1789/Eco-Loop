import uuid

from MCP.protocol import (
    MCPRequest,
    MCPResponse,
    ToolCall,
    ToolResult,
    ToolDefinition,
)
from MCP.registry import ToolRegistry
from MCP.tools import MCPTools
from MCP.database_tool import DatabaseTool


class MCPServer:
    """
    Lightweight MCP Server

    Responsibilities
    ----------------
    - Register all available tools
    - Execute MCP requests
    - Return MCP responses
    """

    def __init__(self):

        self.registry = ToolRegistry()

        self.tools = MCPTools()

        self.database = DatabaseTool()

        self._register_tools()

    # ------------------------------------------------------------------

    def _register_tools(self):

        # ==============================================================
        # Energy Simulation
        # ==============================================================

        self.registry.register(

            ToolDefinition(

                name="simulate_building",

                description="Run an EnergyPlus simulation for a building.",

                input_schema={
                    "type": "object",
                    "properties": {
                        "building_name": {
                            "type": "string"
                        },
                        "weather_file": {
                            "type": "string"
                        },
                        "idf_file": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "building_name"
                    ]
                }

            ),

            self.tools.simulate_building

        )

        # ==============================================================
        # Optimization
        # ==============================================================

        self.registry.register(

            ToolDefinition(

                name="optimize_building",

                description="Optimize the building energy consumption.",

                input_schema={
                    "type": "object",
                    "properties": {
                        "building_name": {
                            "type": "string"
                        },
                        "weather_file": {
                            "type": "string"
                        },
                        "idf_file": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "building_name"
                    ]
                }

            ),

            self.tools.optimize_building

        )

        # ==============================================================
        # Health
        # ==============================================================

        self.registry.register(

            ToolDefinition(

                name="health_check",

                description="Check server health.",

                input_schema={
                    "type": "object",
                    "properties": {}
                }

            ),

            self.tools.health_check

        )

        # ==============================================================
        # Database Tools
        # ==============================================================

        self.registry.register(

            ToolDefinition(

                name="get_buildings",

                description="Return all buildings.",

                input_schema={
                    "type": "object",
                    "properties": {}
                }

            ),

            self.database.get_buildings

        )

        self.registry.register(

            ToolDefinition(

                name="get_building",

                description="Retrieve building information.",

                input_schema={
                    "type": "object",
                    "properties": {
                        "building_name": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "building_name"
                    ]
                }

            ),

            self.database.get_building

        )

        self.registry.register(

            ToolDefinition(

                name="get_zones",

                description="Retrieve all zones in a building.",

                input_schema={
                    "type": "object",
                    "properties": {
                        "building_name": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "building_name"
                    ]
                }

            ),

            self.database.get_zones

        )

        self.registry.register(

            ToolDefinition(

                name="latest_sensor_values",

                description="Retrieve latest sensor readings.",

                input_schema={
                    "type": "object",
                    "properties": {
                        "building_name": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "building_name"
                    ]
                }

            ),

            self.database.latest_sensor_values

        )

    # ------------------------------------------------------------------

    def available_tools(self):
        """
        Returns ToolDefinition objects.
        """

        return self.registry.list_tools()

    # ------------------------------------------------------------------

    def tool_descriptions(self):
        """
        JSON serializable tool descriptions for the LLM.
        """

        tools = []

        for tool in self.registry.list_tools():

            tools.append({

                "name": tool.name,

                "description": tool.description,

                "input_schema": tool.input_schema

            })

        return tools

    # ------------------------------------------------------------------

    def execute_request(
        self,
        request: MCPRequest
    ):

        response = MCPResponse(
            request_id=request.request_id
        )

        for tool_call in request.tool_calls:

            handler = self.registry.get_handler(
                tool_call.tool
            )

            if handler is None:

                response.results.append(

                    ToolResult(

                        id=tool_call.id,

                        success=False,

                        error=f"Unknown tool '{tool_call.tool}'"

                    )

                )

                continue

            try:

                result = handler(
                    **tool_call.arguments
                )

                response.results.append(

                    ToolResult(

                        id=tool_call.id,

                        success=True,

                        result=result

                    )

                )

            except Exception as e:

                response.results.append(

                    ToolResult(

                        id=tool_call.id,

                        success=False,

                        error=str(e)

                    )

                )

        return response

    # ------------------------------------------------------------------

    def execute(
        self,
        tool_name,
        **kwargs
    ):
        """
        Compatibility wrapper used by AgentExecutor.
        """

        request = MCPRequest(

            request_id=str(uuid.uuid4()),

            tool_calls=[

                ToolCall(

                    id=str(uuid.uuid4()),

                    tool=tool_name,

                    arguments=kwargs

                )

            ]

        )

        response = self.execute_request(
            request
        )

        result = response.results[0]

        return {

            "success": result.success,

            "result": result.result,

            "error": result.error

        }

    # ------------------------------------------------------------------

    def get_tool_definition(
        self,
        tool_name
    ):

        return self.registry.get_definition(
            tool_name
        )

    # ------------------------------------------------------------------

    def has_tool(
        self,
        tool_name
    ):

        return self.registry.get_handler(
            tool_name
        ) is not None