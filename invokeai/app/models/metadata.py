from typing import Optional
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr


class ImageMetadata(BaseModel):
    """
    Core generation metadata for an image/tensor generated in InvokeAI.

    Also includes any metadata from the image's PNG tEXt chunks.

    Generated by traversing the execution graph, collecting the parameters of the nearest ancestors of a given node.

    Full metadata may be accessed by querying for the session in the `graph_executions` table.
    """

    positive_conditioning: Optional[StrictStr] = Field(
        default=None, description="The positive conditioning."
    )
    negative_conditioning: Optional[StrictStr] = Field(
        default=None, description="The negative conditioning."
    )
    width: Optional[StrictInt] = Field(
        default=None, description="Width of the image/tensor in pixels."
    )
    height: Optional[StrictInt] = Field(
        default=None, description="Height of the image/tensor in pixels."
    )
    seed: Optional[StrictInt] = Field(
        default=None, description="The seed used for noise generation."
    )
    cfg_scale: Optional[StrictFloat] = Field(
        default=None, description="The classifier-free guidance scale."
    )
    steps: Optional[StrictInt] = Field(
        default=None, description="The number of steps used for inference."
    )
    scheduler: Optional[StrictStr] = Field(
        default=None, description="The scheduler used for inference."
    )
    model: Optional[StrictStr] = Field(
        default=None, description="The model used for inference."
    )
    strength: Optional[StrictFloat] = Field(
        default=None,
        description="The strength used for image-to-image/tensor-to-tensor.",
    )
    image: Optional[StrictStr] = Field(
        default=None, description="The ID of the initial image."
    )
    tensor: Optional[StrictStr] = Field(
        default=None, description="The ID of the initial tensor."
    )
    # Pending model refactor:
    # vae: Optional[str] = Field(default=None,description="The VAE used for decoding.")
    # unet: Optional[str] = Field(default=None,description="The UNet used dor inference.")
    # clip: Optional[str] = Field(default=None,description="The CLIP Encoder used for conditioning.")
    extra: Optional[StrictStr] = Field(
        default=None, description="Extra metadata, extracted from the PNG tEXt chunk."
    )