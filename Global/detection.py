# Copyright (c) Microsoft Corporation

import torchvision.transforms as transforms
from PIL import Image, ImageFile
import torch.nn.functional as F
import torchvision as tv
import numpy as np
import warnings
import argparse
import torch
import gc
import os

from .detection_models import networks


tensor2image = transforms.ToPILImage()

warnings.filterwarnings("ignore", category=UserWarning)

ImageFile.LOAD_TRUNCATED_IMAGES = True


def data_transforms(img, full_size, method=Image.BICUBIC):
    if full_size == "full_size":
        ow, oh = img.size
        h = int(round(oh / 16) * 16)
        w = int(round(ow / 16) * 16)
        if (h == oh) and (w == ow):
            return img
        return img.resize((w, h), method)

    elif full_size == "scale_256":
        ow, oh = img.size
        pw, ph = ow, oh
        if ow < oh:
            ow = 256
            oh = ph / pw * 256
        else:
            oh = 256
            ow = pw / ph * 256

        h = int(round(oh / 16) * 16)
        w = int(round(ow / 16) * 16)
        if (h == ph) and (w == pw):
            return img
        return img.resize((w, h), method)


def scale_tensor(img_tensor, default_scale=256):
    _, _, w, h = img_tensor.shape
    if w < h:
        ow = default_scale
        oh = h / w * default_scale
    else:
        oh = default_scale
        ow = w / h * default_scale

    oh = int(round(oh / 16) * 16)
    ow = int(round(ow / 16) * 16)

    return F.interpolate(img_tensor, [ow, oh], mode="bilinear")


def blend_mask(img, mask):

    np_img = np.array(img).astype("float")

    return Image.fromarray(
        (np_img * (1 - mask) + mask * 255.0).astype("uint8")
    ).convert("RGB")


def main(config: argparse.Namespace, input_image: Image):

    model = networks.UNet(
        in_channels=1,
        out_channels=1,
        depth=4,
        conv_num=2,
        wf=6,
        padding=True,
        batch_norm=True,
        up_mode="upsample",
        with_tanh=False,
        sync_bn=True,
        antialiasing=True,
    )

    ## load model
    checkpoint_path = os.path.join(
        os.path.dirname(__file__), "checkpoints/detection/FT_Epoch_latest.pt"
    )
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state"])
    print("model weights loaded")

    if torch.cuda.is_available() and config.GPU >= 0:
        model.to(config.GPU)
    else:
        model.cpu()

    model.eval()

    print("processing...")

    transformed_image_PIL = data_transforms(input_image, config.input_size)
    input_image = transformed_image_PIL.convert("L")
    input_image = tv.transforms.ToTensor()(input_image)
    input_image = tv.transforms.Normalize([0.5], [0.5])(input_image)
    input_image = torch.unsqueeze(input_image, 0)

    _, _, ow, oh = input_image.shape
    scratch_image_scale = scale_tensor(input_image)

    if torch.cuda.is_available() and config.GPU >= 0:
        scratch_image_scale = scratch_image_scale.to(config.GPU)
    else:
        scratch_image_scale = scratch_image_scale.cpu()

    with torch.no_grad():
        P = torch.sigmoid(model(scratch_image_scale))

    P = P.data.cpu()
    P = F.interpolate(P, [ow, oh], mode="nearest")

    scratch_mask = torch.clamp((P >= 0.4).float(), 0.0, 1.0) * 255

    gc.collect()
    torch.cuda.empty_cache()
    return tensor2image(scratch_mask[0].byte()), transformed_image_PIL


def global_detection(
    input_image: Image,
    gpu: int,
    input_size: str,
) -> Image:

    config = argparse.Namespace()
    config.GPU = gpu
    config.input_size = input_size

    return main(config, input_image)
