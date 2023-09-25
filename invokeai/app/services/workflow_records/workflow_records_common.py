from typing import Any, TypeAlias


class WorkflowNotFoundError(Exception):
    """Raised when a workflow is not found"""


Workflow: TypeAlias = dict[str, Any]
"""Workflows are stored without a schema, so we use a type alias to represent them."""
