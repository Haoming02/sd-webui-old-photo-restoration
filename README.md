<h1 align = "center">W.I.P</h1>
<p align = "center">Currently only installs the requirements</p>

# SD Webui Bringing-Old-Photos-Back-to-Life

> Original Paper: https://arxiv.org/abs/2004.09484

> Original Repo: https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life

#### Install
- On the first launch, this will automatically clone the repository to `~webui\repositories\BOP-BtL`
- Then, it will download the needed 1 model and 2 checkpoints *(~3 GB)*
  > This will take several minutes
- Lastly, it will install all required Python packages
  > Most of them should already exist in the base webui

Alternatively, you can manually download the requirements first by following the [description](https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life#installation) of the original repo.
> Remember to clone to `~webui\repositories\BOP-BtL` instead

#### Uninstall
Delete the following folders:
- `~webui\extensions\sd-webui-old-photo-restoration`
- `~webui\repositories\BOP-BtL`
- `~webui\repositories\Synchronized-BatchNorm-PyTorch`
