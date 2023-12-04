from modules.launch_utils import git_clone, repo_dir, requirements_met
import requests
import launch
import shutil
import zipfile
import bz2
import io
import os

REPO_URL = 'https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life'
SBNPT = 'https://github.com/vacancy/Synchronized-BatchNorm-PyTorch'

LANDMARK = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
FACE_CHECKPOINT = 'https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life/releases/download/v1.0/face_checkpoints.zip'
GLOBAL_CHECKPOINT= 'https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life/releases/download/v1.0/global_checkpoints.zip'

repo_folder = repo_dir('BOP-BtL')
sbnpt_folder = repo_dir('Synchronized-BatchNorm-PyTorch')


print('\nChecking Requirements for Bringing-Old-Photos-Back-to-Life...')


if not os.path.exists(repo_folder):
    git_clone(REPO_URL, repo_dir(repo_folder), "Bringing-Old-Photos-Back-to-Life")
    git_clone(SBNPT, repo_dir(sbnpt_folder), "Synchronized-BatchNorm-PyTorch")

    sync_batchnorm = os.path.join(repo_dir(sbnpt_folder), 'sync_batchnorm')
    networks = os.path.join(repo_dir(repo_folder), 'Face_Enhancement', 'models', 'networks', 'sync_batchnorm')
    models = os.path.join(repo_dir(repo_folder), 'Global', 'detection_models', 'sync_batchnorm')

    if not os.path.exists(networks):
        os.mkdir(networks)
    if not os.path.exists(models):
        os.mkdir(models)

    for script in os.listdir(sync_batchnorm):
        shutil.copy(os.path.join(sync_batchnorm, script), networks)
        shutil.copy(os.path.join(sync_batchnorm, script), models)


face_detection_model = os.path.join(repo_dir(repo_folder), 'Face_Detection', 'shape_predictor_68_face_landmarks.dat')
if not os.path.exists(face_detection_model):
    print('Downloading Landmark Detection Pretrained Model...')
    response = requests.get(LANDMARK)
    bz2_content = response.content

    with open(face_detection_model, 'wb') as output_file:
        decompressed_content = bz2.decompress(bz2_content)
        output_file.write(decompressed_content)


if not os.path.exists(os.path.join(repo_dir(repo_folder), 'Face_Enhancement', 'checkpoints')):
    print('Downloading FACE CHECKPOINT...')
    target_dir = os.path.join(repo_dir(repo_folder), 'Face_Enhancement')
    response = requests.get(FACE_CHECKPOINT)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
        zip_ref.extractall(target_dir)


if not os.path.exists(os.path.join(repo_dir(repo_folder), 'Global', 'checkpoints')):
    print('Downloading GLOBAL CHECKPOINT...')
    target_dir = os.path.join(repo_dir(repo_folder), 'Global')
    response = requests.get(GLOBAL_CHECKPOINT)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
        zip_ref.extractall(target_dir)


requirements = os.path.join(repo_folder, 'requirements.txt')
if not requirements_met(requirements):
    with open(requirements, 'r', encoding='utf8') as REQs:
        packages = REQs.readlines()
        for package in packages:
            if not launch.is_installed(package):
                launch.run_pip(f"install {package}", f"BOP-BoL Requirement: {package}")


print('Requirements for Bringing-Old-Photos-Back-to-Life Installed...\n')
