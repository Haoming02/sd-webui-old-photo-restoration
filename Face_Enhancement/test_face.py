# Copyright (c) Microsoft Corporation.

from collections import OrderedDict
import torchvision.utils as vutils
import warnings
import os

from .options.test_options import TestOptions
from .models.pix2pix_model import Pix2PixModel
from .util.visualizer import Visualizer
from .data import create_dataloader

warnings.filterwarnings("ignore", category=UserWarning)

def test_face(custom_args:list):
    import sys
    cache = sys.argv[1:]
    sys.argv[1:] = custom_args
    opt = TestOptions().parse()
    sys.argv[1:] = cache

    dataloader = create_dataloader(opt)

    model = Pix2PixModel(opt)
    model.eval()

    visualizer = Visualizer(opt)


    single_save_url = os.path.join(opt.checkpoints_dir, opt.name, opt.results_dir, "each_img")


    if not os.path.exists(single_save_url):
        os.makedirs(single_save_url)


    for i, data_i in enumerate(dataloader):
        if i * opt.batchSize >= opt.how_many:
            break

        generated = model(data_i, mode="inference")

        img_path = data_i["path"]

        for b in range(generated.shape[0]):
            img_name = os.path.split(img_path[b])[-1]
            save_img_url = os.path.join(single_save_url, img_name)

            vutils.save_image((generated[b] + 1) / 2, save_img_url)
