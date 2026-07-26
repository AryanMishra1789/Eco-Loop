from copy import deepcopy


class AgentExecutor:
    """
    Agent Executor

    Responsibilities
    ----------------
    - Execute a single MCP tool
    - Store execution context
    - Update memory
    - Maintain execution history
    """

    def __init__(
        self,
        mcp_server,
        memory
    ):

        self.mcp = mcp_server

        self.memory = memory

        self.reset()

    # ---------------------------------------------------------

    def reset(self):

        self.context = {}

        self.history = []

    # ---------------------------------------------------------

    def execute_single_tool(
        self,
        tool_name,
        arguments
    ):
        """
        Execute one tool through the MCP server.
        """

        resolved_arguments = self._resolve_context(arguments)

        self.memory.add_tool_call(
            tool=tool_name,
            arguments=resolved_arguments
        )

        response = self.mcp.execute(
            tool_name,
            **resolved_arguments
        )

        if response["success"]:

            self.context[tool_name] = deepcopy(
                response["result"]
            )

            self.memory.add_observation(
                tool=tool_name,
                result=response["result"]
            )

        self.history.append({

            "tool": tool_name,

            "arguments": deepcopy(
                resolved_arguments
            ),

            "response": deepcopy(
                response
            )

        })

        return response

    # ---------------------------------------------------------

    def _resolve_context(
        self,
        arguments
    ):
        """
        Replace context references.

        Example:

            "$simulate_building.energy"

        with the actual value from a previous tool.
        """

        resolved = {}

        for key, value in arguments.items():

            if (
                isinstance(value, str)
                and value.startswith("$")
            ):

                resolved[key] = self._lookup(
                    value[1:]
                )

            else:

                resolved[key] = value

        return resolved

    # ---------------------------------------------------------

    def _lookup(
        self,
        reference
    ):
        """
        Resolve context path.

        Example

            simulate_building.energy

        """

        parts = reference.split(".")

        if not parts:

            return None

        current = self.context.get(parts[0])

        if current is None:

            return None

        for part in parts[1:]:

            if isinstance(current, dict):

                current = current.get(part)

            else:

                return None

        return current

    # ---------------------------------------------------------

    def execution_context(self):

        return deepcopy(self.context)

    # ---------------------------------------------------------

    def execution_history(self):

        return deepcopy(self.history)

    # ---------------------------------------------------------

    def clear(self):

        self.reset()