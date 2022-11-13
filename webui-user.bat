@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS= --xformers --force-enable-xformers --medvram --api --deepdanbooru
call webui.bat
