from scripts.main_function import bop
from modules import script_callbacks
import gradio as gr


def bop_ui():
    with gr.Blocks() as BOP:
        with gr.Row():
            with gr.Column():
                img_input = gr.Textbox(
                    max_lines=1,
                    label="Input",
                    placeholder="Absolute Path to the Input Folder",
                    interactive=True,
                )
                img_output = gr.Textbox(
                    value="",
                    max_lines=1,
                    label="Output",
                    placeholder="Absolute Path to the Output Folder",
                    interactive=True,
                )

                run_btn = gr.Button(value="Process", variant="primary")

                with gr.Row():
                    with gr.Column():
                        is_scratch = gr.Checkbox(label="Process Scratch")
                        is_hr = gr.Checkbox(label="High Resolution")

                    with gr.Column():
                        face_res = gr.Checkbox(label="Face Restore")
                        del_itr = gr.Checkbox(label="Delete Intermediate Steps")

                    gpu_id = gr.Number(value=0, label="GPU ID", precision=0)

            with gr.Column():
                results = gr.Gallery(label="Results", show_download_button=True)
                with gr.Row():
                    send_i2i = gr.Button(value="Send to img2img")
                    send_inp = gr.Button(value="Send to Inpaint")
                    send_i2e = gr.Button(value="Send to Extras")

        run_btn.click(
            bop,
            inputs=[
                img_input,
                img_output,
                gpu_id,
                is_scratch,
                is_hr,
                face_res,
                del_itr,
            ],
            outputs=[results],
        )

        send_i2i.click(None, None, None, _js="() => {sendImage2Webui('img2img');}")

        send_inp.click(None, None, None, _js="() => {sendImage2Webui('inpaint');}")

        send_i2e.click(None, None, None, _js="() => {sendImage2Webui('extras');}")

    return [(BOP, "BOP", "sd-webui-old-photo-restoration")]


script_callbacks.on_ui_tabs(bop_ui)
