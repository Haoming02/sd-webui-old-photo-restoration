from Global.test import global_test
from Global.detection import global_detection

from Face_Detection.detect_all_dlib import detect
from Face_Detection.detect_all_dlib_HR import detect_hr
from Face_Detection.align_warp_back_multiple_dlib import align_warp
from Face_Detection.align_warp_back_multiple_dlib_HR import align_warp_hr

from Face_Enhancement.test_face import test_face

from modules import scripts
import datetime
import shutil
import os


GLOBAL_CHECKPOINTS_FOLDER = os.path.join(scripts.basedir(), 'Global', 'checkpoints', 'restoration')
FACE_CHECKPOINTS_FOLDER = os.path.join(scripts.basedir(), 'Face_Enhancement', 'checkpoints')
FACE_ENHANCEMENT_CHECKPOINTS = ['Setting_9_epoch_100', 'FaceSR_512']


def validate_paths(input_path: str, output_path: str) -> bool:
    if (not input_path) or (not output_path):
        print("Empty Path Detected...")
        return False

    if input_path == output_path:
        print("Bruh...")
        return False

    if not (os.path.isabs(input_path) and os.path.isabs(output_path)):
        print("Path is not Absolute...")
        return False

    if not os.path.exists(input_path):
        print("Input Path does not Exist!")
        return False

    if not os.path.exists(output_path):
        print("Output Path does not Exist!")
        return False

    if len(input_path.split()) > 1:
        print("Empty spaces detected in Input Path!")
        return False

    if len(output_path.split()) > 1:
        print("Empty spaces detected in Output Path!")
        return False

    if len(os.listdir(input_path)) == 0:
        print("No files found in Input Path!")
        return False

    return True


def core_functions(input_path:str, output_path:str, gpu_id:int, scratch:bool, hr:bool, face_res:bool):
    final_output = os.path.join(output_path, 'final_output')
    if not os.path.exists(final_output):
        os.makedirs(final_output)

    import torch
    if not torch.cuda.is_available():
        gpu_id = -1

    # ===== Stage 1 =====
    print("Running Stage 1: Overall restoration")
    stage1_output = os.path.join(output_path, 'stage1')

    if not scratch:
        args = ['--test_mode', 'Full', '--Quality_restore', '--test_input', input_path, '--outputs_dir', stage1_output, '--gpu_ids', str(gpu_id)]
        global_test(args, GLOBAL_CHECKPOINTS_FOLDER)

    else:
        mask_dir = os.path.join(stage1_output, "masks")
        new_input = os.path.join(mask_dir, "input")
        new_mask = os.path.join(mask_dir, "mask")
        args = ['--test_path', input_path, '--output_dir', mask_dir, '--input_size', 'full_size', '--GPU', str(gpu_id)]
        global_detection(args)

        args = ['--Scratch_and_Quality_restore', '--test_input', new_input, '--test_mask', new_mask, '--outputs_dir', stage1_output, '--gpu_ids', str(gpu_id)]
        if hr:
            args.append('--HR')

        global_test(args, GLOBAL_CHECKPOINTS_FOLDER)

    stage1_results = os.path.join(stage1_output, "restored_image")
    for FILE in os.listdir(stage1_results):
        shutil.copy(os.path.join(stage1_results, FILE), final_output)

    if not face_res:
        print("Processing is done. Please check the results.")
        return final_output

    # ===== Stage 2 =====
    print("Running Stage 2: Face Detection")
    stage2_output = os.path.join(output_path, 'stage2')

    if hr:
        detect_hr(['--url', stage1_results, '--save_url', stage2_output])
    else:
        detect(['--url', stage1_results, '--save_url', stage2_output])

    # ===== Stage 3 =====
    print("Running Stage 3: Face Enhancement")
    stage_3_input_face = stage2_output
    stage_3_output_dir = os.path.join(output_path, 'stage3')

    if hr:
        args = [
            '--checkpoints_dir', FACE_CHECKPOINTS_FOLDER, '--old_face_folder', stage_3_input_face,
            '--name', FACE_ENHANCEMENT_CHECKPOINTS[1], '--gpu_ids', str(gpu_id),
            '--load_size', '512', '--label_nc', '18', '--no_instance', '--preprocess_mode', 'resize',
            '--batchSize', '1', '--results_dir', stage_3_output_dir, '--no_parsing_map'
        ]
    else:
        args = [
            '--checkpoints_dir', FACE_CHECKPOINTS_FOLDER, '--old_face_folder', stage_3_input_face,
            '--name', FACE_ENHANCEMENT_CHECKPOINTS[0], '--gpu_ids', str(gpu_id),
            '--load_size', '256', '--label_nc', '18', '--no_instance', '--preprocess_mode', 'resize',
            '--batchSize', '4', '--results_dir', stage_3_output_dir, '--no_parsing_map'
        ]

    test_face(args)

    stage3_results = os.path.join(stage_3_output_dir, "each_img")

    # ===== Stage 4 =====
    print("Running Stage 4: Blending")

    args = ['--origin_url', stage1_results, '--replace_url', stage3_results, '--save_url', final_output]
    if hr:
        align_warp_hr(args)
    else:
        align_warp(args)

    print("All the processing is done. Please check the results.")
    return final_output


def bop(input_path: str, output_path: str, gpu_id: int, scratch: bool, hr: bool, face_res: bool, del_itr: bool) -> list:
    if not validate_paths(input_path.strip(), output_path.strip()):
        return []

    output_path = os.path.join(output_path, datetime.datetime.now().strftime("%m%d-%H.%M.%S"))

    final_outputs: str = core_functions(input_path, output_path, gpu_id, scratch, hr, face_res)

    if not del_itr:
        results = [os.path.join(final_outputs, F) for F in os.listdir(final_outputs)]
        return results

    else:
        for PATH in os.listdir(output_path):
            if "final_output" not in PATH:
                shutil.rmtree(os.path.join(output_path, PATH))

        for FILE in os.listdir(final_outputs):
            os.rename(
                os.path.join(final_outputs, FILE), os.path.join(output_path, FILE)
            )
        os.rmdir(final_outputs)

        results = [os.path.join(output_path, F) for F in os.listdir(output_path)]
        return results
