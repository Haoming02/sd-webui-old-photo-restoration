# Copyright (c) Microsoft Corporation

import torchvision.transforms as T
import warnings

from .options.test_options import TestOptions
from .models.pix2pix_model import Pix2PixModel
from .data import create_dataloader

warnings.filterwarnings("ignore", category=UserWarning)
tensor2image = T.ToPILImage()


def test_face(face_images: list, args: dict) -> list:
    opt = TestOptions().parse()
    for K, V in args.items():
        setattr(opt, K, V)

    dataloader = create_dataloader(opt, face_images)
    images = []

    model = Pix2PixModel(opt)
    model.eval()

    for i, data_i in enumerate(dataloader):
        if i * opt.batchSize >= opt.how_many:
            break

        generated = model(data_i, mode="inference")

        for b in range(generated.shape[0]):
            images.append(tensor2image((generated[b] + 1) / 2))

    return images
