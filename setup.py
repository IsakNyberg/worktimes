from cx_Freeze import setup, Executable
import os
import sys
import tkinter
os.environ['TCL_LIBRARY'] ="C:\\Users\\Isak\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] ="C:\\Users\\Isak\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

#includethese=["C:\\Users\\Isak\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl86t.lib", "C:\\Users\\Isak\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk86t.lib"]

base = None

if sys.platform == 'win32':
    base = "Win32GUI"



setup(
    name="Work Times",
    version="0.1",
    description="Work times",
    options={"build_exe": {"packages":["tkinter"],"include_files": ["vcruntime140.dll","tcl86t.dll","tk86t.dll","tcl86t.lib","tk86t.lib","icon.ico"]}},
    executables=[Executable("work_times.py",base=base, icon="icon.ico")])
