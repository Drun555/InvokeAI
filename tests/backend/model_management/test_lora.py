import time

import pytest

from invokeai.backend.model_management.lora import ModelPatcher
from invokeai.backend.model_management.models.base import BaseModelType, ModelType, SubModelType
from invokeai.backend.util.test_utils import install_and_load_model


@pytest.mark.slow
def test_apply_lora(model_installer, torch_device):
    lora_start = time.time()
    lora_info = install_and_load_model(
        model_installer=model_installer,
        model_path_id_or_url="TODO",
        model_name="VoxelXL_v1",
        base_model=BaseModelType.StableDiffusionXL,
        model_type=ModelType.Lora,
    )
    unet_start = time.time()
    print(f"Loaded LoRA from disk in {unet_start - lora_start}s")

    unet_info = install_and_load_model(
        model_installer=model_installer,
        model_path_id_or_url="TODO",
        model_name="stable-diffusion-xl-base-1-0",
        base_model=BaseModelType.StableDiffusionXL,
        model_type=ModelType.Main,
        submodel_type=SubModelType.UNet,
    )
    unet_done = time.time()
    print(f"Loaded UNet from disk in {unet_done - unet_start}s")

    with ModelPatcher.apply_lora_unet(unet_info.context.model, [(lora_info.context.model, 0.5)]):
        patch_done = time.time()
        print(f"Lora applied to UNet in {patch_done - unet_done}s")
        with unet_info as unet:
            unet_to_cuda_done = time.time()
            print(f"UNet to cuda took {unet_to_cuda_done - patch_done}s")
            pass

    ctx_done = time.time()
    print(f"Full context took {ctx_done - unet_done}s")
    assert False
