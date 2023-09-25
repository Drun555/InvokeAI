from abc import ABC, abstractmethod

from invokeai.app.services.workflow_records.workflow_records_common import Workflow


class WorkflowRecordsStorageBase(ABC):
    """Base class for workflow storage services."""

    @abstractmethod
    def get(self, workflow_id: str) -> Workflow:
        """Get workflow by id."""
        pass

    @abstractmethod
    def create(self, workflow: Workflow) -> Workflow:
        """Creates a workflow."""
        pass
