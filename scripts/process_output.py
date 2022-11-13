from turtle import back
import modules.scripts as scripts
from launch import run_pip
import importlib.util

import gradio as gr

from modules import images
from modules.processing import process_images, Processed
from modules.shared import opts, cmd_opts, state
from PIL import Image, ImageOps


class Script(scripts.Script):
    def title(self):
        return "Process Output"

    

    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):
        angle = gr.Slider(minimum=0.0, maximum=360.0, step=1, value=0,
                          label="Angle (Counter-Clockwise)")
        hflip = gr.Checkbox(False, label="Horizontal flip")
        vflip = gr.Checkbox(False, label="Vertical flip")
        fill = gr.Checkbox(False, label="Fill")
        background = gr.Checkbox(False, label="Background Removal")
        trim = gr.Slider(minimum=0.0, maximum=100.0, step=0.1, value=0, label="Trim (Percentage)")
        add_border = gr.Number(default="0", label="Desired Border+Image Size (Padded out to 1:1)")
        overwrite = gr.Checkbox(False, label="Save transformed image only")

        return [angle, hflip, vflip, fill, background, trim, add_border, overwrite]


    def run(self, p, angle, hflip, vflip, fill, background, trim, add_border, overwrite):
        print("PIL Processing Script Loaded")
            
        # function which takes an image, an angle and two booleans indicating horizontal and vertical flips, then returns the image rotated and flipped accordingly
        def rotate_and_resize(im, angle, hflip, vflip, fill, trim, add_border):
            raf = im
            if angle != 0:
                raf = raf.rotate(angle, expand=fill, resample = Image.BICUBIC, fillcolor = (255, 255, 255))
            if hflip:
                raf = raf.transpose(Image.FLIP_LEFT_RIGHT)
            if vflip:
                raf = raf.transpose(Image.FLIP_TOP_BOTTOM)
            if trim:
                trim = (trim/100)*raf.height if raf.height == raf.width else (trim/100)*raf.width if raf.width < raf.height else (trim/100)*raf.height
                raf = ImageOps.crop(raf, trim)
            if add_border != 0 or add_border is not None:
                add_border = int(add_border)
                raf = ImageOps.expand(raf, (int((add_border - raf.width)/2), int((add_border - raf.height)/2)), fill=(255, 255, 255))
            return raf    
        
        if(background):
            from rembg import remove
        
        
        if overwrite:
            p.do_not_save_samples = True

        suffix = ""

        if angle != 0:
            suffix += "_rotated_" + str(angle)
            p.extra_generation_params.update({"rotation angle": str(angle)})
        if hflip:
            suffix += "_hflip"
            p.extra_generation_params.update({"horizontally flipped": str(hflip)})
        if vflip:
            suffix += "_vflip"
            p.extra_generation_params.update({"vertically flipped": str(vflip)})
        if fill:
            suffix += "_fill"
            p.extra_generation_params.update({"filled on rotate": str(fill)})
        if trim:
            suffix += "_trim_" + str(trim)
            p.extra_generation_params.update({"trimmed (%)": str(trim)})
        if add_border:
            suffix += "_resize_" + str(add_border)
            p.extra_generation_params.update({"padded to": str(add_border)})
        if background:
            suffix += "_background_removed"
            p.extra_generation_params.update({"background removed": str(background)})
        
        state.job_count = p.n_iter
        p.n_iter = 1
        images_list = []
        seeds = []
        
        # Process each image
        for i in range(state.job_count):
            proc = process_images(p)
            for j in range(len(proc.images)):
                transformed = rotate_and_resize(proc.images[j], angle, hflip, vflip, fill, trim, add_border)
                if background:
                    transformed = remove(transformed, alpha_matting=True)
                images_list.append(transformed)                
                images.save_image(transformed, p.outpath_samples, "",
                    p.seed, proc.prompt, opts.samples_format, info= proc.info, p=p, suffix=suffix)
                seeds.append(p.seed)
                p.seed += 1
                    
        return Processed(p, images_list, p.seed, "")
