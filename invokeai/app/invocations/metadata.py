from typing import Any, Optional, Union

from pydantic import BaseModel, Field

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    FieldDescriptions,
    InputField,
    InvocationContext,
    OutputField,
    UIType,
    invocation,
    invocation_output,
)

from ...version import __version__


class MetadataItemField(BaseModel):
    label: str = Field(description=FieldDescriptions.metadata_item_label)
    value: Any = Field(description=FieldDescriptions.metadata_item_value)


@invocation_output("metadata_item_output")
class MetadataItemOutput(BaseInvocationOutput):
    """Metadata Item Output"""

    item: MetadataItemField = OutputField(description="Metadata Item")


@invocation("metadata_item", title="Metadata Item", tags=["metadata"], category="metadata", version="1.0.0")
class MetadataItemInvocation(BaseInvocation):
    """Used to create an arbitrary metadata item. Provide "label" and make a connection to "value" to store that data as the value."""

    label: str = InputField(description=FieldDescriptions.metadata_item_label)
    value: Any = InputField(description=FieldDescriptions.metadata_item_value, ui_type=UIType.Any)

    def invoke(self, context: InvocationContext) -> MetadataItemOutput:
        return MetadataItemOutput(item=MetadataItemField(label=self.label, value=self.value))


class MetadataField(BaseModel):
    """
    Pydantic model for metadata with custom root of type dict[str, Any].
    Workflows are stored without a strict schema.
    """

    __root__: dict[str, Any] = Field(description="A dictionary of metadata, shape of which is arbitrary")

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        return super().dict(*args, **kwargs)["__root__"]


@invocation_output("metadata_output")
class MetadataOutput(BaseInvocationOutput):
    metadata: MetadataField = OutputField(description="Metadata Dict")


@invocation("metadata", title="Metadata", tags=["metadata"], category="metadata", version="1.0.0")
class MetadataInvocation(BaseInvocation):
    """Takes a MetadataItem or collection of MetadataItems and outputs a MetadataDict."""

    items: Union[list[MetadataItemField], MetadataItemField] = InputField(
        description=FieldDescriptions.metadata_item_polymorphic
    )

    def invoke(self, context: InvocationContext) -> MetadataOutput:
        if isinstance(self.items, MetadataItemField):
            # single metadata item
            data = {self.items.label: self.items.value}
        else:
            # collection of metadata items
            data = {item.label: item.value for item in self.items}

        # add app version
        data.update({"app_version": __version__})
        return MetadataOutput(metadata=MetadataField(__root__=data))


@invocation("merge_metadata", title="Metadata Merge", tags=["metadata"], category="metadata", version="1.0.0")
class MergeMetadataInvocation(BaseInvocation):
    """Merged a collection of MetadataDict into a single MetadataDict."""

    collection: list[MetadataField] = InputField(description=FieldDescriptions.metadata_collection)

    def invoke(self, context: InvocationContext) -> MetadataOutput:
        data = {}
        for item in self.collection:
            data.update(item.dict())

        return MetadataOutput(metadata=MetadataField(__root__=data))


class WithMetadata(BaseModel):
    metadata: Optional[MetadataField] = InputField(default=None, description=FieldDescriptions.metadata)
