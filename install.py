import launch
import os

EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))
flag = False

requirements = os.path.join(EXTENSION_FOLDER, 'requirements.txt')
with open(requirements, 'r', encoding='utf8') as REQs:
    packages = REQs.readlines()

    for package in packages:
        package = package.strip()

        if not launch.is_installed(package):
            if not flag:
                print('\nInstalling Requirements for Bringing-Old-Photos-Back-to-Life...')
                flag = True

            launch.run_pip(f"install {package}", f"Old-Photo-Restoration Requirement: {package}")
