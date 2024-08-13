from modules.script_callbacks import on_app_started
from modules.api.models import *
from modules.api import api

from fastapi import FastAPI, Body
import gradio as gr

from scripts.main_function import main


def bop_api(_: gr.Blocks, app: FastAPI):

    @app.post("/bop")
    async def old_photo_restoration(
        image: str = Body("", title="input image"),
        scratch: bool = Body(False, title="process scratch"),
        hr: bool = Body(False, title="high resolution"),
        face_res: bool = Body(False, title="face restore"),
        cpu: bool = Body(False, title="force CPU"),
    ):
        if not image:
            return

        input_image = api.decode_base64_to_image(image)

        img = main(input_image, scratch, hr, face_res, cpu)

        return {"image": api.encode_pil_to_base64(img).decode("utf-8")}


on_app_started(bop_api)
