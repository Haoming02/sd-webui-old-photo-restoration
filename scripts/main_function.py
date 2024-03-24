from Global.test import global_test
# from Global.detection import global_detection

# from Face_Detection.detect_all_dlib import detect
# from Face_Detection.detect_all_dlib_HR import detect_hr
# from Face_Detection.align_warp_back_multiple_dlib import align_warp
# from Face_Detection.align_warp_back_multiple_dlib_HR import align_warp_hr

# from Face_Enhancement.test_face import test_face

from modules import scripts
from PIL import Image
import datetime
import shutil
import os


GLOBAL_CHECKPOINTS_FOLDER = os.path.join(
    scripts.basedir(), "Global", "checkpoints", "restoration"
)
FACE_CHECKPOINTS_FOLDER = os.path.join(
    scripts.basedir(), "Face_Enhancement", "checkpoints"
)
FACE_ENHANCEMENT_CHECKPOINTS = ("Setting_9_epoch_100", "FaceSR_512")

GPU_ID = -1


def main(input_image: Image, scratch: bool, hr: bool, face_res: bool) -> Image:
    input_image = input_image.convert("RGB")
    # outpath = opts.outdir_samples or opts.outdir_extras_samples

    # ===== Stage 1 =====
    print("Running Stage 1: Overall restoration")
    if not scratch:
        args = [
            "--test_mode",
            "Full",
            "--Quality_restore",
            "--gpu_ids",
            str(GPU_ID),
        ]

        return global_test(GLOBAL_CHECKPOINTS_FOLDER, args, input_image)

    else:
        raise NotImplementedError
        mask_dir = os.path.join(stage1_output, "masks")
        new_input = os.path.join(mask_dir, "input")
        new_mask = os.path.join(mask_dir, "mask")
        args = [
            "--test_path",
            input_path,
            "--output_dir",
            mask_dir,
            "--input_size",
            "full_size",
            "--GPU",
            str(gpu_id),
        ]
        global_detection(args)

        args = [
            "--Scratch_and_Quality_restore",
            "--test_input",
            new_input,
            "--test_mask",
            new_mask,
            "--outputs_dir",
            stage1_output,
            "--gpu_ids",
            str(gpu_id),
        ]
        if hr:
            args.append("--HR")

        global_test(args, GLOBAL_CHECKPOINTS_FOLDER)

    stage1_results = os.path.join(stage1_output, "restored_image")
    for FILE in os.listdir(stage1_results):
        shutil.copy(os.path.join(stage1_results, FILE), final_output)

    if not face_res:
        print("Processing is done. Please check the results.")
        return final_output
    else:
        raise NotImplementedError
    # ===== Stage 2 =====
    print("Running Stage 2: Face Detection")
    stage2_output = os.path.join(output_path, "stage2")

    if hr:
        detect_hr(["--url", stage1_results, "--save_url", stage2_output])
    else:
        detect(["--url", stage1_results, "--save_url", stage2_output])

    # ===== Stage 3 =====
    print("Running Stage 3: Face Enhancement")
    stage_3_input_face = stage2_output
    stage_3_output_dir = os.path.join(output_path, "stage3")

    if hr:
        args = [
            "--checkpoints_dir",
            FACE_CHECKPOINTS_FOLDER,
            "--old_face_folder",
            stage_3_input_face,
            "--name",
            FACE_ENHANCEMENT_CHECKPOINTS[1],
            "--gpu_ids",
            str(gpu_id),
            "--load_size",
            "512",
            "--label_nc",
            "18",
            "--no_instance",
            "--preprocess_mode",
            "resize",
            "--batchSize",
            "1",
            "--results_dir",
            stage_3_output_dir,
            "--no_parsing_map",
        ]
    else:
        args = [
            "--checkpoints_dir",
            FACE_CHECKPOINTS_FOLDER,
            "--old_face_folder",
            stage_3_input_face,
            "--name",
            FACE_ENHANCEMENT_CHECKPOINTS[0],
            "--gpu_ids",
            str(gpu_id),
            "--load_size",
            "256",
            "--label_nc",
            "18",
            "--no_instance",
            "--preprocess_mode",
            "resize",
            "--batchSize",
            "4",
            "--results_dir",
            stage_3_output_dir,
            "--no_parsing_map",
        ]

    test_face(args)

    stage3_results = os.path.join(stage_3_output_dir, "each_img")

    # ===== Stage 4 =====
    print("Running Stage 4: Blending")

    args = [
        "--origin_url",
        stage1_results,
        "--replace_url",
        stage3_results,
        "--save_url",
        final_output,
    ]
    if hr:
        align_warp_hr(args)
    else:
        align_warp(args)

    print("All the processing is done. Please check the results.")
    return final_output
