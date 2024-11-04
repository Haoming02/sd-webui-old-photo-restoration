from modules.ui_components import InputAccordion
from modules import scripts_postprocessing
import gradio as gr

from scripts.bopb2l_main import main


class OldPhotoRestoration(scripts_postprocessing.ScriptPostprocessing):
    name = "BOP"
    order = 200409484

    def ui(self):
        with InputAccordion(False, label="Old Photo Restoration") as enable:
            proc_order = gr.Radio(
                choices=("Restoration First", "Upscale First"),
                value="Restoration First",
                label="Processing Order",
            )

            with gr.Row():
                do_scratch = gr.Checkbox(False, label="Process Scratch")
                do_face_res = gr.Checkbox(False, label="Face Restore")
            with gr.Row():
                is_hr = gr.Checkbox(False, label="High Resolution")
                use_cpu = gr.Checkbox(True, label="Use CPU")

        args = {
            "enable": enable,
            "proc_order": proc_order,
            "do_scratch": do_scratch,
            "do_face_res": do_face_res,
            "is_hr": is_hr,
            "use_cpu": use_cpu,
        }

        return args

    def process_firstpass(self, pp: scripts_postprocessing.PostprocessedImage, **args):

        if args["enable"] and args["proc_order"] == "Restoration First":

            do_scratch: bool = args["do_scratch"]
            do_face_res: bool = args["do_face_res"]
            is_hr: bool = args["is_hr"]
            use_cpu: bool = args["use_cpu"]

            img = pp.image
            pp.image = main(img, do_scratch, is_hr, do_face_res, use_cpu)

    def process(self, pp: scripts_postprocessing.PostprocessedImage, **args):

        if args["enable"] and args["proc_order"] == "Upscale First":

            do_scratch: bool = args["do_scratch"]
            do_face_res: bool = args["do_face_res"]
            is_hr: bool = args["is_hr"]
            use_cpu: bool = args["use_cpu"]

            img = pp.image
            pp.image = main(img, do_scratch, is_hr, do_face_res, use_cpu)
