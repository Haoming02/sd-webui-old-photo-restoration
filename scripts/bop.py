from modules.launch_utils import repo_dir
from modules import script_callbacks
from modules import scripts
from subprocess import run
import gradio as gr
import datetime
import sys
import os

par = os.path.dirname
OUTPUT_FOLDER = os.path.join(par(par(scripts.basedir())), 'outputs', 'old-photo-restoration')

python = os.path.join(par(sys.executable), 'activate')

if os.path.exists(python):
    py = [python, '&&', 'python']
else:
    py = [str(sys.executable)]

repo_folder = repo_dir('BOP-BtL')
app = os.path.join(repo_folder, 'run.py')

def catch_old_results(output_folder:str):
    if not os.path.exists(output_folder):
        return {}
    return {f: os.path.getmtime(os.path.join(output_folder, f)) for f in os.listdir(output_folder)}

def detect_new_results(output_folder:str, existing_files:dict):
    new_files = {f: os.path.getmtime(os.path.join(output_folder, f)) for f in os.listdir(output_folder)}
    return [os.path.join(output_folder, f) for f, time in new_files.items() if f not in existing_files or existing_files[f] < time]

def bop(img_path:str, gpu_id:int, scratch:bool, hr:bool):
    if(len(img_path.strip()) < 1):
        return []

    img_path = os.path.abspath(img_path)

    if not os.path.exists(img_path):
        print('Invalid Path!')
        return []

    if len(os.listdir(img_path)) == 0:
        print('Empty Path!')
        return []

    if len(img_path.split()) > 1:
        print('Space Detected in Path!')
        return []

    main_environment = os.getcwd()
    process_output = os.path.join(OUTPUT_FOLDER, datetime.datetime.now().strftime("%m.%d-%H.%M.%S"))
    final_output = os.path.join(process_output, 'final_output')
    cache = catch_old_results(final_output)

    os.chdir(repo_folder)

    cmd = py + [app, '--GPU', str(gpu_id), '--input_folder', img_path, '--output_folder', process_output]

    if scratch:
        cmd.append('--with_scratch')
    if hr:
        cmd.append('--HR')

    # print(' '.join(cmd))

    run(cmd, shell=True)

    os.chdir(main_environment)
    results = detect_new_results(final_output, cache)
    return results

def bop_ui():
    with gr.Blocks() as BOP:
        with gr.Row():
            with gr.Column():
                img_input = gr.Textbox (max_lines=1, label='Input', info='Enter the Absolute Path to the Images', interactive=True)

                run_btn = gr.Button(value='Process', variant='primary')

                with gr.Row():
                    gpu_id = gr.Number(value=0, label="GPU ID", precision=0)
                    with gr.Column():
                        is_scratch = gr.Checkbox(label="With Scratch")
                        is_hr = gr.Checkbox(label="High Resolution")

            with gr.Column():
                img_output = gr.Gallery(label='Output', show_download_button=True)
                with gr.Row():
                    send_i2i = gr.Button(value='Send to img2img')
                    send_inp = gr.Button(value='Send to Inpaint')
                    send_i2e = gr.Button(value='Send to Extras')

        run_btn.click(bop, inputs=[img_input, gpu_id, is_scratch, is_hr], outputs=[img_output])

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
