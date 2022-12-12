@echo off

set SAFETENSORS_FAST_GPU=1
set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS= --xformers --medvram --clip-models-path D:\StableDiffusion_Repositories\voldy\venv\Lib\site-packages\open_clip

call webui.bat
