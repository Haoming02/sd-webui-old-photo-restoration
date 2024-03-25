# Copyright (c) Microsoft Corporation

import torch.utils.data
from .face_dataset import FaceTestDataset


def create_dataloader(opt, faces: list):

    instance = FaceTestDataset()
    instance.initialize(opt, faces)

    print(
        f"Dataset [{type(instance).__name__}] with {len(instance)} faces was created..."
    )

    dataloader = torch.utils.data.DataLoader(
        instance,
        batch_size=opt.batchSize,
        shuffle=not opt.serial_batches,
        num_workers=int(opt.nThreads),
        drop_last=opt.isTrain,
    )

    return dataloader
