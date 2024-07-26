import launch
import os

try:
    import dlib
except ModuleNotFoundError:
    launch.run_pip("install dlib-bin", "Old-Photo-Restoration Requirement: dlib")


EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))
requirements = os.path.join(EXTENSION_FOLDER, "requirements.txt")

with open(requirements, "r", encoding="utf-8") as REQs:
    packages = REQs.readlines()

    for package in packages:

        if not launch.is_installed(package.strip()):
            launch.run_pip(f"install {package}", f"Old-Photo-Restoration Requirement: {package}")
