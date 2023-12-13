from Global.test import main

from modules import script_callbacks
from modules import scripts
import gradio as gr
import datetime
import os

par = os.path.dirname

GLOBAL_CHECKPOINTS_FOLDER = os.path.join(scripts.basedir(), 'Global', 'checkpoints', 'restoration')

DEFAULT_OUTPUT_FOLDER = os.path.join(par(par(scripts.basedir())), 'outputs', 'old-photo-restoration')
if not os.path.exists(DEFAULT_OUTPUT_FOLDER):
    os.mkdir(DEFAULT_OUTPUT_FOLDER)

def validate_paths(input_path:str, output_path:str):
    if not os.path.exists(input_path):
        print('Input Path does not Exist!')
        return False

    if not os.path.exists(output_path):
        print('Output Path does not Exist!')
        return False

    if len(input_path.split()) > 1:
        print('Empty spaces detected in Input Path!')
        return False

    if len(output_path.split()) > 1:
        print('Empty spaces detected in Output Path!')
        return False

    if len(os.listdir(input_path)) == 0:
        print('No files found in Input Path!')
        return False

    return True

def bop(img_path:str, output_path:str, gpu_id:int, scratch:bool, hr:bool):
    if(len(img_path.strip()) < 1 or len(output_path.strip()) < 1):
        return []

    img_path = os.path.abspath(img_path)
    output_path = os.path.abspath(output_path)

    if not validate_paths(img_path, output_path):
        return []

    process_output = os.path.join(output_path, datetime.datetime.now().strftime("%m.%d-%H.%M.%S"))

    if not scratch:
        args = ['--test_mode', 'Full', '--Quality_restore', '--test_input', str(img_path), '--outputs_dir', str(process_output), '--gpu_ids', str(gpu_id)]

    main(args, GLOBAL_CHECKPOINTS_FOLDER)

    final_output = os.path.join(process_output, 'restored_image')
    results = [os.path.join(final_output, F) for F in os.listdir(final_output)]
    return results

def bop_ui():
    with gr.Blocks() as BOP:
        with gr.Row():
            with gr.Column():
                img_input = gr.Textbox(max_lines=1, label='Input', info='Enter the Absolute Path to the Input Folder', interactive=True)
                img_output = gr.Textbox(value=DEFAULT_OUTPUT_FOLDER, max_lines=1, label='Output', info='Enter the Absolute Path to the Output Folder', interactive=True)

                run_btn = gr.Button(value='Process', variant='primary')

                with gr.Row():
                    gpu_id = gr.Number(value=0, label="GPU ID", precision=0)
                    with gr.Column():
                        is_scratch = gr.Checkbox(label="With Scratch")
                        is_hr = gr.Checkbox(label="High Resolution")

            with gr.Column():
                results = gr.Gallery(label='Results', show_download_button=True)
                with gr.Row():
                    send_i2i = gr.Button(value='Send to img2img')
                    send_inp = gr.Button(value='Send to Inpaint')
                    send_i2e = gr.Button(value='Send to Extras')

        run_btn.click(bop, inputs=[img_input, img_output, gpu_id, is_scratch, is_hr], outputs=[results])

        send_i2i.click(None, None, None,
            _js="() => {sendImage2Webui('img2img');}",
        )

        send_inp.click(None, None, None,
            _js="() => {sendImage2Webui('inpaint');}",
        )

        send_i2e.click(None, None, None,
            _js="() => {sendImage2Webui('extras');}",
        )

    return [(BOP, 'BOP', 'sd-webui-old-photo-restoration')]

script_callbacks.on_ui_tabs(bop_ui)
