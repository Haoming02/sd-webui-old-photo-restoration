import os

EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))

FACE = os.path.join(
    EXTENSION_FOLDER,
    "lib_bopb2l",
    "Face_Enhancement",
    "checkpoints",
)
GLOBAL = os.path.join(
    EXTENSION_FOLDER,
    "lib_bopb2l",
    "Global",
    "checkpoints",
)
MDL = os.path.join(
    EXTENSION_FOLDER,
    "lib_bopb2l",
    "Face_Detection",
    "shape_predictor_68_face_landmarks.dat",
)

if not os.path.exists(FACE):
    print("\n[Warning] face_checkpoints not detected! Please download it from Release!")
if not os.path.exists(GLOBAL):
    print("[Warning] global_checkpoints not detected! Please download it from Release!")
if not os.path.exists(MDL):
    print("[Warning] face_landmarks not detected! Please download it from Release!\n")
