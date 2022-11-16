from cx_Freeze import setup, Executable

buildOptions = dict(packages=['tkinter'])

exe = [Executable('./src/app.py', 
    base='Win32GUI', 
    targetName="OrdSaveCodeLoader.exe",
    icon="static/icon.ico"
    )]

setup(
    name='ordSaveCodeLoader', 
    version="0.0.6",
    author="s4ng",
    description="원랜디 세이브 코드 로더",
    options=dict(build_exe = buildOptions),
    executables=exe
)
