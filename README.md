# SD Webui Old Photo Restoration
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which allows you to perform **Bringing-Old-Photos-Back-to-Life** natively.

> Compatible with [Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)

<p align="center">
<img src="UI.png">
</p>

> Original Paper: https://arxiv.org/abs/2004.09484

> Original Repo: https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life *(includes some example images)*

## Requirements
0. Install this Extension[*](#extension-not-showing-up)
1. Download `global_checkpoints.zip` from [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases)
2. Extract and put the `checkpoints` **folder** *(not just the files)* into `~webui/extensions/sd-webui-old-photo-restoration/Global`
3. Download `face_checkpoints.zip` from [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases)
4. Extract and put the `checkpoints` **folder** *(not just the files)* into `~webui/extensions/sd-webui-old-photo-restoration/Face_Enhancement`
5. Download `shape_predictor_68_face_landmarks.zip` from [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases)
6. Extract the `.dat` **file** into `~webui/extensions/sd-webui-old-photo-restoration/Face_Detection`

> The [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases) page includes the original links, as well as the backups mirrored by myself

> Another mirror: [Google Drive](https://drive.google.com/drive/folders/1CXAgAYQzz_JkMmxqcabvgGhG_msyMkyS)

## Extension not Showing Up
If after installing the Extension, nothing shows up in the **Extras** tab, it's usually caused by failing to install the `dlib` package. To solve it:

#### Linux
From my brief searching, you need to install `cmake` first, then try installing `dlib` again

```bash
pip install dlib
```
or
```bash
sudo apt-get install cmake
```

#### Windows

<ins><b>Easier</b> Way</ins>

- Install the pre-built package from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x

<ins><b>Intended</b> Way</ins>

- Install [Visual Studio](https://visualstudio.microsoft.com/vs/community/) with
    - [**C++**](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation?view=msvc-170) component
    - [**CMake**](https://learn.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio?view=msvc-170) component

## How to Use
After installing this Extension, there will be an **Old Photo Restoration** section in the **Extras** tab

0. Expand the dropdown to enable the features
1. Upload the image(s) to be processed
2. Adjust the settings as needed
3. Click **Generate**
4. The result(s) will show up on the right once the process finishes

## Settings
- **Processing Order:** Choose between upscaling the image first or perform the restoration first
- **Process Scratch:** Remove scratches from the image
- **Face Restore:** Use a pre-trained model to improve the faces
  - *(This is **different** from the Webui built-in ones)*
- **High Resolution:** Use higher parameters to do the processing
  - *(Only has an effect when either `Process Scratch` or `Face Restore` is also enabled)*
