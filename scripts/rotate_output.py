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
        angle = gr.Slider(minimum=0.0, maximum=360.0, step=1, value=0,
                          label="Angle")
        hflip = gr.Checkbox(False, label="Horizontal flip")
        vflip = gr.Checkbox(False, label="Vertical flip")
        overwrite = gr.Checkbox(False, label="Overwrite existing files")


        return [angle, hflip, vflip, overwrite]


    def run(self, p, angle, hflip, vflip, overwrite):
        print("Rotating output")
        # function which takes an image, an angle and two booleans indicating horizontal and vertical flips, then returns the image rotated and flipped accordingly
        def rotate_and_flip(im, angle, hflip, vflip):
            raf = im
            if angle != 0:
                raf = raf.rotate(angle, expand=False, resample = Image.BICUBIC, fillcolor = (255, 255, 255))
            if hflip:
                raf = raf.transpose(Image.FLIP_LEFT_RIGHT)
            if vflip:
                raf = raf.transpose(Image.FLIP_TOP_BOTTOM)
            return raf
            
        basename = ""

        if(not overwrite):
            if angle != 0:
                basename += "rotated_" + str(angle)
            if hflip:
                basename += "_hflip"
            if vflip:
                basename += "_vflip"
            else:
                p.do_not_save_samples = True

        proc = process_images(p)
        
        # rotate and flip each image in the processed images
        for i in range(len(proc.images)):

            proc.images[i] = rotate_and_flip(proc.images[i], angle, hflip, vflip)

            images.save_image(proc.images[i], p.outpath_samples, basename,
            proc.seed + i, proc.prompt, opts.samples_format, info= proc.info, p=p)
            
        return proc
