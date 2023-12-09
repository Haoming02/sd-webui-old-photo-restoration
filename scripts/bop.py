from modules.launch_utils import repo_dir
from modules import script_callbacks
from modules import scripts
from subprocess import run
import gradio as gr
import datetime
import sys
import os

par = os.path.dirname
DEFAULT_OUTPUT_FOLDER = os.path.join(par(par(scripts.basedir())), 'outputs', 'old-photo-restoration')
if not os.path.exists(DEFAULT_OUTPUT_FOLDER):
    os.mkdir(DEFAULT_OUTPUT_FOLDER)

python = os.path.join(par(sys.executable), 'activate')

if os.path.exists(python):
    if os.name == 'nt': 
        py = [python, '&&', 'python'] # Windows
    else: 
        py = ['source', python, '&&', 'python'] # Unix
else:
    py = [str(sys.executable)]

repo_folder = repo_dir('BOP-BtL')
app = os.path.join(repo_folder, 'run.py')

def force_install_requirements():
    import launch
    requirements = os.path.join(repo_folder, 'requirements.txt')
    with open(requirements, 'r', encoding='utf8') as REQs:
        packages = REQs.readlines()
        for package in packages:
            package = package.strip()
            if not launch.is_installed(package):
                launch.run_pip(f"install {package}", f"BOP-BoL Requirement: {package}")

    print('Requirements Installed... Please ReloadUI!')

def bop(img_path:str, output_path:str, gpu_id:int, scratch:bool, hr:bool):
    if(len(img_path.strip()) < 1 or len(output_path.strip()) < 1):
        return []

    img_path = os.path.abspath(img_path)
    output_path = os.path.abspath(output_path)

    if not os.path.exists(img_path):
        print('Invalid Input Path!')
        return []

    if not os.path.exists(output_path):
        print('Invalid Output Path!')
        return []

    if len(img_path.split()) > 1:
        print('Space Detected in Input Path!')
        return []

    if len(output_path.split()) > 1:
        print('Space Detected in Output Path!')
        return []

    if len(os.listdir(img_path)) == 0:
        print('Empty Input Path!')
        return []

    main_environment = os.getcwd()
    process_output = os.path.join(output_path, datetime.datetime.now().strftime("%m.%d-%H.%M.%S"))
    final_output = os.path.join(process_output, 'final_output')

    os.chdir(repo_folder)

    cmd = py + [app, '--GPU', str(gpu_id), '--input_folder', img_path, '--output_folder', process_output]

    if scratch:
        cmd.append('--with_scratch')
    if hr:
        cmd.append('--HR')

    # print(' '.join(cmd))

    run(cmd, shell=True)

    os.chdir(main_environment)
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

        install = gr.Button(value="Force Install Requirements")
        install.click(fn=force_install_requirements)

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
