import modules.scripts as scripts
import gradio as gr

from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):

    def title(self):
        return "Custom code"


    # Determines when the script should be shown in the dropdown menu via the returned value. 
    # is_img2img is True if the current tab is img2img, and False if it is txt2img. Thus, return 
    # is_img2img to only show the script on the img2img tab.
    def show(self, is_img2img):
        return cmd_opts.allow_code


    # How the script's parameters are displayed in the UI. See https://gradio.app/docs/#components 
    # for the different elements you can use and how to specify them. The returned parameters 
    # are passed to the run method.
    def ui(self, is_img2img):
        code = gr.Textbox(label="Python code", lines=1)

        return [code]


    def run(self, p, code):
        assert cmd_opts.allow_code, '--allow-code option must be enabled'

        display_result_data = [[], -1, ""]

        def display(imgs, s=display_result_data[1], i=display_result_data[2]):
            display_result_data[0] = imgs
            display_result_data[1] = s
            display_result_data[2] = i

        from types import ModuleType
        compiled = compile(code, '', 'exec')
        module = ModuleType("testmodule")
        module.__dict__.update(globals())
        module.p = p
        module.display = display
        exec(compiled, module.__dict__)

        return Processed(p, *display_result_data)
    
    