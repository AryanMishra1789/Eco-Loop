from copy import deepcopy
from datetime import datetime

class AgentMemory:
    """
    Short-term memory for a single agent execution.

    Stores:
        - Goal
        - Conversation
        - Tool Calls
        - Tool Observations
        - Final Response
        - Execution Metadata
    """

    def __init__(self):

        self.reset()

    # ---------------------------------------------------------

    def reset(self):

        self.goal = None

        self.messages = []

        self.tool_calls = []

        self.observations = []

        self.final_response = None

        self.status = "running"

        self.iteration = 0

        self.created_at = datetime.utcnow().isoformat()

        self.updated_at = self.created_at

    # ---------------------------------------------------------

    def _touch(self):

        self.updated_at = datetime.utcnow().isoformat()

    # ---------------------------------------------------------

    def set_goal(self, goal):

        self.goal = goal

        self._touch()

    # ---------------------------------------------------------

    def increment_iteration(self):

        self.iteration += 1

        self._touch()

    # ---------------------------------------------------------

    def add_message(
        self,
        role,
        content
    ):

        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

        self._touch()

    # ---------------------------------------------------------

    def add_tool_call(
        self,
        tool,
        arguments
    ):

        self.tool_calls.append({
            "tool": tool,
            "arguments": deepcopy(arguments),
            "timestamp": datetime.utcnow().isoformat()
        })

        self._touch()

    # ---------------------------------------------------------

    def add_observation(
        self,
        tool,
        result
    ):

        self.observations.append({
            "tool": tool,
            "result": deepcopy(result),
            "timestamp": datetime.utcnow().isoformat()
        })

        self._touch()

    # ---------------------------------------------------------

    def latest_observation(self):

        if not self.observations:
            return None

        return deepcopy(self.observations[-1])

    # ---------------------------------------------------------

    def latest_tool_call(self):

        if not self.tool_calls:
            return None

        return deepcopy(self.tool_calls[-1])

    # ---------------------------------------------------------

    def set_final_response(
        self,
        response
    ):

        self.final_response = response

        self.status = "completed"

        self._touch()

    # ---------------------------------------------------------

    def fail(self):

        self.status = "failed"

        self._touch()

    # ---------------------------------------------------------

    def summary(self):

        return {
            "goal": self.goal,
            "status": self.status,
            "iteration": self.iteration,
            "messages": deepcopy(self.messages),
            "tool_calls": deepcopy(self.tool_calls),
            "observations": deepcopy(self.observations),
            "final_response": self.final_response,
            "metadata": {
                "created_at": self.created_at,
                "updated_at": self.updated_at
            }
        }

    # ---------------------------------------------------------

    def __str__(self):

        return str(self.summary())