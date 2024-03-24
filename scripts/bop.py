from scripts.main_function import main
from modules import scripts_postprocessing, ui_components
import gradio as gr


class FaceSwapScriptExtras(scripts_postprocessing.ScriptPostprocessing):
    name = "BOP"
    order = 200409484

    def ui(self):
        with ui_components.InputAccordion(
            False, label="Old Photo Restoration"
        ) as enable:

            with gr.Row():
                is_scratch = gr.Checkbox(label="Process Scratch")
                face_res = gr.Checkbox(label="Face Restore")
                is_hr = gr.Checkbox(label="High Resolution")

            with gr.Row():
                del_itr = gr.Checkbox(label="Delete Intermediate Steps")
                ups_fst = gr.Checkbox(label="Upscale before Restoration")
                gr.Markdown(
                    '<p><a style="color: cyan; text-decoration: underline;" href="https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life#1-full-pipeline">[Doc]</a></p>'
                )

        args = {
            "enable": enable,
            "is_scratch": is_scratch,
            "face_res": face_res,
            "is_hr": is_hr,
            "del_itr": del_itr,
            "ups_fir": ups_fst,
        }

        return args

    def process_firstpass(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        enable: bool = args["enable"]
        is_scratch: bool = args["is_scratch"]
        face_res: bool = args["face_res"]
        is_hr: bool = args["is_hr"]
        del_itr: bool = args["del_itr"]
        ups_fst: bool = args["ups_fir"]
        pass

    def process(self, pp: scripts_postprocessing.PostprocessedImage, **args):

        img = pp.image
        pp.image = main(img, False, False, False)
