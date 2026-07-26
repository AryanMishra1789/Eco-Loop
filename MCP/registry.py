from typing import Callable, Dict

from MCP.protocol import ToolDefinition


class ToolRegistry:

    def __init__(self):

        self._definitions: Dict[str, ToolDefinition] = {}

        self._handlers: Dict[str, Callable] = {}

    # -----------------------------------------------------

    def register(
        self,
        definition: ToolDefinition,
        handler: Callable
    ):

        self._definitions[
            definition.name
        ] = definition

        self._handlers[
            definition.name
        ] = handler

    # -----------------------------------------------------

    def get_definition(
        self,
        tool_name
    ):

        return self._definitions.get(tool_name)

    # -----------------------------------------------------

    def get_handler(
        self,
        tool_name
    ):

        return self._handlers.get(tool_name)

    # -----------------------------------------------------

    def list_tools(self):

        return list(
            self._definitions.values()
        )