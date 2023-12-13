function sendImage2Webui(webuiTab) {
    const extension_tab = document.getElementById('tab_sd-webui-old-photo-restoration');
    const img = extension_tab.querySelector('img');

    if (img === null)
        return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;

    ctx.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);
    let imageInput = null;

    switch (webuiTab) {
        case "img2img":
            switch_to_img2img();
            imageInput = gradioApp().getElementById('mode_img2img').querySelector("input[type='file']");
            break;
        case "extras":
            switch_to_extras();
            imageInput = gradioApp().getElementById('mode_extras').querySelector("input[type='file']");
            break;
        case "inpaint":
            switch_to_inpaint();
            imageInput = gradioApp().getElementById('img2img_inpaint_tab').querySelector("input[type='file']");
            break;
    }

    canvas.toBlob((blob) => {
        const file = new File(([blob]), "restored.png");
        setImageOnInput(imageInput, file);
    });
}

function setImageOnInput(imageInput, file) {

    const dt = new DataTransfer();
    dt.items.add(file);
    const list = dt.files;

    imageInput.files = list;

    const event = new Event('change', {
        'bubbles': true,
        "composed": true
    });

    imageInput.dispatchEvent(event);
}
