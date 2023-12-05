# SD Webui Bringing-Old-Photos-Back-to-Life
<h3 align="right"><i>W.I.P</i></h3>

> Original Paper: https://arxiv.org/abs/2004.09484

> Original Repo: https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life

**Important:** Currently only supports webui with virtual environment, not the standalone release with embedded Python

**Important:** Currently the `Send to img2img` and `Send to Inpaint` buttons do nothing

## How to Use
After installing this Extension, there will be a new **`BOP`** tab on top. 
Enter the **absolute path** to a folder containing the input images, then click **Process** to start.
- You can also specify the `GPU ID` *(Enter `-1` to use CPU)*
- You can also toggle scratches processing and high resolution inputs *(Check the original repo for more info)*

### Install
- On the first launch, this will automatically clone the repository to `~webui\repositories\BOP-BtL`
- Then, it will download the needed 1 model and 2 checkpoints *(~3 GB)*
  > This will take several minutes
- Lastly, it will install all required Python packages
  > Most of them should already exist in the base webui

Alternatively, you can manually download the requirements first by following the [description](https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life#installation) of the original repo.
> Remember to clone to `~webui\repositories\BOP-BtL` instead

### Uninstall
Delete the following folders:
- `~webui\extensions\sd-webui-old-photo-restoration`
- `~webui\repositories\BOP-BtL`
- `~webui\repositories\Synchronized-BatchNorm-PyTorch`
- `~webui\outputs\old-photo-restoration`

## To Do
- [ ] Implement `Send to img2img` and `Send to Inpaint`
- [ ] Directly access the models instead of calling the awful scripts
    > This will also solve the freaking virtual environment issues
