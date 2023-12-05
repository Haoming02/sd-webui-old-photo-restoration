# SD Webui Old Photo Restoration 
This is an Extension for the [Automatic1111 Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui), which allows you to perform **Bringing-Old-Photos-Back-to-Life** from the webui, 
and then send the output into `img2img` or `Inpaint` for further touch-up.

> Original Paper: https://arxiv.org/abs/2004.09484

> Original Repo: https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life

## How to Use
After installing this Extension, there will be a new **`BOP`** tab on top. 
Enter the **absolute path** to a folder containing the input images, then click **Process** to start.
- The path needs to be an **absolute path** that directly points to the folder, and the path should contain **no spaces**
- You can also specify the `GPU ID` to use
- You can also toggle **scratches** processing and **high resolution** processing
    - Check the original repo for more info
- The outputs are saved to `~webui\outputs\old-photo-restoration`
- Some sample images are included at `~webui\repositories\BOP-BtL\test_images`

### Install
- On the first launch, this will automatically clone the repository to `~webui\repositories\BOP-BtL`
- Then, it will download the needed 1 model and 2 checkpoints *(~3 GB)*
  > This will take several minutes
- Lastly, it will install all required Python packages

### Uninstall
Delete the following folders:
- `~webui\extensions\sd-webui-old-photo-restoration`
- `~webui\repositories\BOP-BtL`
- `~webui\repositories\Synchronized-BatchNorm-PyTorch`
- `~webui\outputs\old-photo-restoration`

## To Do
- [X] Implement `Send to img2img` and `Send to Inpaint`
- [X] Add support for standalone release
- [ ] ~~Directly access the models instead of calling the awful scripts~~ On-hold. Might do it in the future...
