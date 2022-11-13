@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS= --xformers --force-enable-xformers --medvram --api --deepdanbooru
set ACCELERATE=TRUE

call webui.bat
