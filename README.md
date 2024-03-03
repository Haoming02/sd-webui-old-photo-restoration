# SD Webui Old Photo Restoration
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which allows you to perform **Bringing-Old-Photos-Back-to-Life** from the webui, 
and then send the output into `img2img` or `Inpaint` for further touch-up.

> Original Paper: https://arxiv.org/abs/2004.09484

> Original Repo: https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life *(includes some example images)*

<p align="center"><img src="sample.jpg"></p>

## Requirements
0. Install this extension
1. Download `global_checkpoints.zip` from [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases)
2. Extract and put the `checkpoints` **folder** *(not just the files)* into `~webui/extensions/sd-webui-old-photo-restoration/Global`
3. Download `face_checkpoints.zip` from [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases)
4. Extract and put the `checkpoints` **folder** *(not just the files)* into `~webui/extensions/sd-webui-old-photo-restoration/Face_Enhancement`
5. Download `shape_predictor_68_face_landmarks.zip` from [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases)
6. Extract the `.dat` **file** into `~webui/extensions/sd-webui-old-photo-restoration/Face_Detection`

> The [Releases](https://github.com/Haoming02/sd-webui-old-photo-restoration/releases) page contains the original links, as well as the backup links mirrored by myself

## How to Use
After installing this Extension, there will be a new **BOP** tab at the top
1. Enter the **absolute path** to a folder containing the input image(s)
2. Enter the **absolute path** to a folder to store the output image(s)
3. Adjust the settings as needed
4. Click **Process** to start
5. The result image(s) will show up on the right once the processes are finished

#### Note
- The path needs to be an **absolute path** with **no spaces**

## Settings
- **Process Scratch:** Fix and remove the scratches from the images
- **Face Restore:** Use the pre-trained model to improve the faces
  - *(This is **not** the built-in ones from the Webui)*
- **High Resolution:** Use higher parameters to do the processing
  - *(Only has an effect when either `Process Scratch` or `Face Restore` is also active)*
- **Delete Intermediate Steps:** Only keep the final results
- **GPU ID:** Specify the GPU to use. Set to `-1` to use CPU instead. Forced to `-1` when no CUDA is detected.
