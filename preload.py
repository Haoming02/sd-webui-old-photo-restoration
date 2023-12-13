import launch
import os

EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))

print('\nChecking Requirements for Bringing-Old-Photos-Back-to-Life...')


FACE = os.path.join(EXTENSION_FOLDER, 'Face_Enhancement', 'checkpoints')
if not os.path.exists(FACE):
    print('[Warning] face_checkpoints not detected! Please download it from Release!')

GLOBAL = os.path.join(EXTENSION_FOLDER, 'Global', 'checkpoints')
if not os.path.exists(GLOBAL):
    print('[Warning] global_checkpoints not detected! Please download it from Release!')

MDL = os.path.join(EXTENSION_FOLDER, 'Face_Detection', 'shape_predictor_68_face_landmarks.dat')
if not os.path.exists(GLOBAL):
    print('[Warning] face_landmarks not detected! Please download it from Release!')


requirements = os.path.join(EXTENSION_FOLDER, 'requirements.txt')
with open(requirements, 'r', encoding='utf8') as REQs:
    packages = REQs.readlines()

    for package in packages:
        package = package.strip()

        if not launch.is_installed(package):
            launch.run_pip(f"install {package}", f"Old-Photo-Restoration Requirement: {package}")
