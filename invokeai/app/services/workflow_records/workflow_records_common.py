from typing import Any

from pydantic import BaseModel, Field


class WorkflowNotFoundError(Exception):
    """Raised when a workflow is not found"""


class WorkflowField(BaseModel):
    """
    Pydantic model for workflows with custom root of type dict[str, Any].
    Workflows are stored without a strict schema.
    """

    __root__: dict[str, Any] = Field(description="Workflow dict")

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        return super().model_dump(*args, **kwargs)["__root__"]
