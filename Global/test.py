# Copyright (c) Microsoft Corporation

import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import torch
import cv2
import os

from .models.mapping_model import Pix2PixHDModel_Mapping
from .options.test_options import TestOptions

tensor2image = transforms.ToPILImage()


def data_transforms(img, method=Image.BILINEAR, scale=False):

    ow, oh = img.size
    pw, ph = ow, oh
    if scale == True:
        if ow < oh:
            ow = 256
            oh = ph / pw * 256
        else:
            oh = 256
            ow = pw / ph * 256

    h = int(round(oh / 4) * 4)
    w = int(round(ow / 4) * 4)

    if (h == ph) and (w == pw):
        return img

    return img.resize((w, h), method)


def data_transforms_rgb_old(img):
    w, h = img.size
    A = img
    if w < 256 or h < 256:
        A = transforms.Scale(256, Image.BILINEAR)(img)
    return transforms.CenterCrop(256)(A)


def irregular_hole_synthesize(img, mask):

    img_np = np.array(img).astype("uint8")
    mask_np = np.array(mask).astype("uint8")
    mask_np = mask_np / 255
    img_new = img_np * (1 - mask_np) + mask_np * 255

    hole_img = Image.fromarray(img_new.astype("uint8")).convert("RGB")

    return hole_img


def parameter_set(opt, ckpt_dir):
    ## Default parameters
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.label_nc = 0
    opt.n_downsample_global = 3
    opt.mc = 64
    opt.k_size = 4
    opt.start_r = 1
    opt.mapping_n_block = 6
    opt.map_mc = 512
    opt.no_instance = True
    opt.checkpoints_dir = ckpt_dir

    if opt.Quality_restore:
        opt.name = "mapping_quality"
        opt.load_pretrainA = os.path.join(opt.checkpoints_dir, "VAE_A_quality")
        opt.load_pretrainB = os.path.join(opt.checkpoints_dir, "VAE_B_quality")
    if opt.Scratch_and_Quality_restore:
        opt.NL_res = True
        opt.use_SN = True
        opt.correlation_renormalize = True
        opt.NL_use_mask = True
        opt.NL_fusion_method = "combine"
        opt.non_local = "Setting_42"
        opt.name = "mapping_scratch"
        opt.load_pretrainA = os.path.join(opt.checkpoints_dir, "VAE_A_quality")
        opt.load_pretrainB = os.path.join(opt.checkpoints_dir, "VAE_B_scratch")
        if opt.HR:
            opt.mapping_exp = 1
            opt.inference_optimize = True
            opt.mask_dilation = 3
            opt.name = "mapping_Patch_Attention"


def global_test(
    ckpt_dir: str, custom_args: list, input_image: Image, mask: Image = None
) -> Image:

    opt = TestOptions().parse(custom_args)

    parameter_set(opt, ckpt_dir)

    model = Pix2PixHDModel_Mapping()

    model.initialize(opt)
    model.eval()

    img_transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
    )
    mask_transform = transforms.ToTensor()

    print("processing...")

    if opt.NL_use_mask:
        if opt.mask_dilation != 0:
            kernel = np.ones((3, 3), np.uint8)
            mask = np.array(mask)
            mask = cv2.dilate(mask, kernel, iterations=opt.mask_dilation)
            mask = Image.fromarray(mask.astype("uint8"))

        input_image = irregular_hole_synthesize(input_image, mask)
        mask = mask_transform(mask)
        mask = mask[:1, :, :]  ## Convert to single channel
        mask = mask.unsqueeze(0)
        input_image = img_transform(input_image)
        input_image = input_image.unsqueeze(0)

    else:
        if opt.test_mode == "Scale":
            input_image = data_transforms(input_image, scale=True)
        elif opt.test_mode == "Full":
            input_image = data_transforms(input_image, scale=False)
        elif opt.test_mode == "Crop":
            input_image = data_transforms_rgb_old(input_image)

        input_image = img_transform(input_image)
        input_image = input_image.unsqueeze(0)
        mask = torch.zeros_like(input_image)

    with torch.no_grad():
        generated = model.inference(input_image, mask)

    restored = torch.clamp((generated.data.cpu() + 1.0) / 2.0, 0.0, 1.0) * 255
    return tensor2image(restored[0].byte())
