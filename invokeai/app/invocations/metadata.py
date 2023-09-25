from typing import Any, Literal, Optional, Union

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    FieldDescriptions,
    InputField,
    InvocationContext,
    MetadataField,
    MetadataItemField,
    OutputField,
    UIType,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.controlnet_image_processors import ControlField
from invokeai.app.invocations.model import MainModelField, VAEModelField

from ...version import __version__


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


@invocation(
    "metadata_accumulator", title="Metadata Accumulator", tags=["metadata"], category="metadata", version="1.0.0"
)
class CoreMetadataInvocation(BaseInvocation):
    """Outputs a Core Metadata Object"""

    generation_mode: Literal["txt2img", "img2img", "inpaint", "outpaint"] = InputField(
        description="The generation mode that output this image",
    )
    positive_prompt: Optional[str] = InputField(default=None, description="The positive prompt parameter")
    negative_prompt: Optional[str] = InputField(default=None, description="The negative prompt parameter")
    width: Optional[int] = InputField(default=None, description="The width parameter")
    height: Optional[int] = InputField(default=None, description="The height parameter")
    seed: Optional[int] = InputField(default=None, description="The seed used for noise generation")
    rand_device: Optional[str] = InputField(default=None, description="The device used for random number generation")
    cfg_scale: Optional[float] = InputField(default=None, description="The classifier-free guidance scale parameter")
    steps: Optional[int] = InputField(default=None, description="The number of steps used for inference")
    scheduler: Optional[str] = InputField(default=None, description="The scheduler used for inference")
    clip_skip: Optional[int] = InputField(
        default=None,
        description="The number of skipped CLIP layers",
    )
    model: MainModelField = InputField(description="The main model used for inference")
    controlnets: list[ControlField] = InputField(description="The ControlNets used for inference")
    # loras: list[LoRAMetadataField] = InputField(description="The LoRAs used for inference")
    strength: Optional[float] = InputField(
        default=None,
        description="The strength used for latents-to-latents",
    )
    init_image: Optional[str] = InputField(
        default=None,
        description="The name of the initial image",
    )
    vae: Optional[VAEModelField] = InputField(
        default=None,
        description="The VAE used for decoding, if the main model's default was not used",
    )

    # SDXL
    positive_style_prompt: Optional[str] = InputField(
        default=None,
        description="The positive style prompt parameter",
    )
    negative_style_prompt: Optional[str] = InputField(
        default=None,
        description="The negative style prompt parameter",
    )

    # SDXL Refiner
    refiner_model: Optional[MainModelField] = InputField(
        default=None,
        description="The SDXL Refiner model used",
    )
    refiner_cfg_scale: Optional[float] = InputField(
        default=None,
        description="The classifier-free guidance scale parameter used for the refiner",
    )
    refiner_steps: Optional[int] = InputField(
        default=None,
        description="The number of steps used for the refiner",
    )
    refiner_scheduler: Optional[str] = InputField(
        default=None,
        description="The scheduler used for the refiner",
    )
    refiner_positive_aesthetic_score: Optional[float] = InputField(
        default=None,
        description="The aesthetic score used for the refiner",
    )
    refiner_negative_aesthetic_score: Optional[float] = InputField(
        default=None,
        description="The aesthetic score used for the refiner",
    )
    refiner_start: Optional[float] = InputField(
        default=None,
        description="The start value used for refiner denoising",
    )

    def invoke(self, context: InvocationContext) -> MetadataOutput:
        """Collects and outputs a CoreMetadata object"""

        return MetadataOutput(metadata=MetadataField(__root__=self.dict()))
