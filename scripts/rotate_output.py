import modules.scripts as scripts
import gradio as gr

from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state
from PIL import Image


class Script(scripts.Script):
    def title(self):
        return "Rotate output"


    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):
        angle = gr.Slider(minimum=0.0, maximum=360.0, step=1, value=0, label="Angle")
        hflip = gr.Checkbox(False, label="Horizontal flip")
        vflip = gr.Checkbox(False, label="Vertical flip")

        return [angle, hflip, vflip]

    def run(self, p, angle, hflip, vflip):
        print("Rotating output")
        # function which takes an image, an angle and two booleans indicating horizontal and vertical flips, then returns the image rotated and flipped accordingly
        def rotate_and_flip(im, angle, hflip, vflip):
            raf = im
            if angle != 0:
                raf = raf.rotate(angle, expand=True)
            if hflip:
                raf = raf.transpose(Image.FLIP_LEFT_RIGHT)
            if vflip:
                raf = raf.transpose(Image.FLIP_TOP_BOTTOM)
            return raf

        proc = process_images(p)
        
        # rotate and flip each image in the processed images
        for i in range(len(proc.images)):
            proc.images[i] = rotate_and_flip(proc.images[i], angle, hflip, vflip)
            
        return proc
