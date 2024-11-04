from lib_bopb2l.Global.test import global_test
from lib_bopb2l.Global.detection import global_detection

from lib_bopb2l.Face_Detection.detect_all_dlib import detect
from lib_bopb2l.Face_Detection.detect_all_dlib_HR import detect_hr
from lib_bopb2l.Face_Detection.align_warp_back_multiple_dlib import align_warp
from lib_bopb2l.Face_Detection.align_warp_back_multiple_dlib_HR import align_warp_hr

from lib_bopb2l.Face_Enhancement.test_face import test_face

from modules import scripts
from PIL import Image
import torch
import os


GLOBAL_CHECKPOINTS_FOLDER = os.path.join(
    scripts.basedir(), "lib_bopb2l", "Global", "checkpoints", "restoration"
)
FACE_CHECKPOINTS_FOLDER = os.path.join(
    scripts.basedir(), "lib_bopb2l", "Face_Enhancement", "checkpoints"
)

FACE_ENHANCEMENT_CHECKPOINTS = ("Setting_9_epoch_100", "FaceSR_512")


def main(
    input_image: Image, scratch: bool, hr: bool, face_res: bool, use_cpu: bool
) -> Image:
    input_image = input_image.convert("RGB")

    gpu_id = 0
    if not torch.cuda.is_available() or use_cpu:
        gpu_id = -1

    # ===== Stage 1 =====
    print("\nRunning Stage 1: Overall restoration")
    if not scratch:
        args = [
            "--test_mode",
            "Full",
            "--Quality_restore",
            "--gpu_ids",
            str(gpu_id),
        ]

        stage1_output = global_test(GLOBAL_CHECKPOINTS_FOLDER, args, input_image)

    else:
        mask, transformed_image = global_detection(input_image, gpu_id, "full_size")

        args = [
            "--Scratch_and_Quality_restore",
            "--gpu_ids",
            str(gpu_id),
        ]

        if hr:
            args.append("--HR")

        stage1_output = global_test(
            GLOBAL_CHECKPOINTS_FOLDER,
            args,
            transformed_image.convert("RGB"),
            mask.convert("RGB"),
        )

    if not face_res:
        print("Processing is done. Please check the results.")
        return stage1_output

    # ===== Stage 2 =====
    print("\nRunning Stage 2: Face Detection")

    if hr:
        faces = detect_hr(stage1_output)
    else:
        faces = detect(stage1_output)

    print(f"Detected {len(faces)} Faces...")

    if len(faces) == 0:
        print("Skipping face restoration...")
        print("Processing is done. Please check the results.")
        return stage1_output

    # ===== Stage 3 =====
    print("\nRunning Stage 3: Face Enhancement")

    if hr:
        args = {
            "checkpoints_dir": FACE_CHECKPOINTS_FOLDER,
            "name": FACE_ENHANCEMENT_CHECKPOINTS[1],
            "gpu_ids": str(gpu_id),
            "load_size": 512,
            "label_nc": 18,
            "no_instance": True,
            "preprocess_mode": "resize",
            "batchSize": 1,
            "no_parsing_map": True,
        }

    else:
        args = {
            "checkpoints_dir": FACE_CHECKPOINTS_FOLDER,
            "name": FACE_ENHANCEMENT_CHECKPOINTS[0],
            "gpu_ids": str(gpu_id),
            "load_size": 256,
            "label_nc": 18,
            "no_instance": True,
            "preprocess_mode": "resize",
            "batchSize": 4,
            "no_parsing_map": True,
        }

    restored_faces = test_face(faces, args)

    # ===== Stage 4 =====
    print("\nRunning Stage 4: Blending")

    if hr:
        final_output = align_warp_hr(stage1_output, restored_faces)
    else:
        final_output = align_warp(stage1_output, restored_faces)

    print("All the processing is done. Please check the results.")
    return final_output
