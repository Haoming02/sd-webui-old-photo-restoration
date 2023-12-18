from Global.test import global_test
from Global.detection import global_detection

from modules import scripts
import datetime
import shutil
import os

GLOBAL_CHECKPOINTS_FOLDER = os.path.join(scripts.basedir(), 'Global', 'checkpoints', 'restoration')

def validate_paths(input_path:str, output_path:str) -> bool:
    if(len(input_path.strip()) < 1 or len(output_path.strip()) < 1):
        print('Empty Path Detected...')
        return False

    try:
        assert (os.path.isabs(input_path) and os.path.isabs(output_path))
    except AssertionError:
        print('Path is not Absolute...')
        return False

    if not os.path.exists(input_path):
        print('Input Path does not Exist!')
        return False

    if not os.path.exists(output_path):
        print('Output Path does not Exist!')
        return False

    if len(input_path.split()) > 1:
        print('Empty spaces detected in Input Path!')
        return False

    if len(output_path.split()) > 1:
        print('Empty spaces detected in Output Path!')
        return False

    if len(os.listdir(input_path)) == 0:
        print('No files found in Input Path!')
        return False

    return True


def core_functions(input_path:str, output_path:str, gpu_id:int, scratch:bool, hr:bool, face_res:bool):
    final_output = os.path.join(output_path, 'final_output')
    if not os.path.exists(final_output):
        os.makedirs(final_output)

    # ===== Stage 1 =====
    stage1_output = os.path.join(output_path, 'stage1')

    if not scratch:
        args = ['--test_mode', 'Full', '--Quality_restore', '--test_input', input_path, '--outputs_dir', stage1_output, '--gpu_ids', str(gpu_id)]
        global_test(args, GLOBAL_CHECKPOINTS_FOLDER)

    else:
        mask_dir = os.path.join(stage1_output, "masks")
        new_mask = os.path.join(mask_dir, "mask")
        args = ['--test_path', input_path, '--output_dir', mask_dir, '--input_size', 'full_size', '--GPU', str(gpu_id)]
        global_detection(args)

        args = ['--Scratch_and_Quality_restore', '--test_input', input_path, '--test_mask', new_mask, '--outputs_dir', stage1_output, '--gpu_ids', str(gpu_id)]
        if hr:
            args.append('--HR')

        global_test(args, GLOBAL_CHECKPOINTS_FOLDER)

    stage1_results = os.path.join(stage1_output, "restored_image")

    if not face_res:
        for FILE in os.listdir(stage1_results):
            shutil.copy(os.path.join(stage1_results, FILE), final_output)
        return final_output

    else:
        print('Face Restoration is not implemented yet...')

    # ===== Stage 2 =====
        pass
    # ===== Stage 3 =====
        pass
    # ===== Stage 4 =====
        pass

    return stage1_results


def bop(input_path:str, output_path:str, gpu_id:int, scratch:bool, hr:bool, face_res:bool, del_itr:bool):
    if not validate_paths(input_path, output_path):
        return []

    output_path = os.path.join(output_path, datetime.datetime.now().strftime("%m-%d %H.%M.%S"))

    final_output = core_functions(input_path, output_path, gpu_id, scratch, hr, face_res)

    if not del_itr:
        results = [os.path.join(final_output, F) for F in os.listdir(final_output)]
        return results

    else:
        for PATH in os.listdir(output_path):
            if 'final_output' not in PATH:
                shutil.rmtree(os.path.join(output_path, PATH))

        for FILE in os.listdir(final_output):
            os.rename(os.path.join(final_output, FILE), os.path.join(output_path, FILE))
        os.rmdir(final_output)

        results = [os.path.join(output_path, F) for F in os.listdir(output_path)]
        return results
