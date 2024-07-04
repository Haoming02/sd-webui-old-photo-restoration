import os

try:
    import dlib
except ModuleNotFoundError:
    print('\n[Old Photo Restoration] Failed to import "dlib" package...')
    print('Please refer to the "Extension not Showing Up" section on the repo...\n')

EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))

FACE = os.path.join(EXTENSION_FOLDER, "Face_Enhancement", "checkpoints")
if not os.path.exists(FACE):
    print("\n[Warning] face_checkpoints not detected! Please download it from Release!")

GLOBAL = os.path.join(EXTENSION_FOLDER, "Global", "checkpoints")
if not os.path.exists(GLOBAL):
    print("[Warning] global_checkpoints not detected! Please download it from Release!")

MDL = os.path.join(EXTENSION_FOLDER, "Face_Detection", "shape_predictor_68_face_landmarks.dat")
if not os.path.exists(MDL):
    print("[Warning] face_landmarks not detected! Please download it from Release!\n")
