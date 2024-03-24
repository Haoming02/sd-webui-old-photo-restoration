# Copyright (c) Microsoft Corporation


def create_model(opt):
    assert opt.model == "pix2pixHD"

    from .pix2pixHD_model import Pix2PixHDModel, InferenceModel

    if opt.isTrain:
        model = Pix2PixHDModel()
    else:
        model = InferenceModel()

    model.initialize(opt)
    if opt.verbose:
        print("model [%s] was created" % (model.name()))

    assert not opt.isTrain

    return model


def create_da_model(opt):
    assert opt.model == "pix2pixHD"

    from .pix2pixHD_model_DA import Pix2PixHDModel, InferenceModel

    if opt.isTrain:
        model = Pix2PixHDModel()
    else:
        model = InferenceModel()

    model.initialize(opt)
    if opt.verbose:
        print("model [%s] was created" % (model.name()))

    assert not opt.isTrain

    return model
