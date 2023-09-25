# Yt-dlp GUI. 
## For download videos from YouTube
![screenshot](https://github.com/GennadiyVick/Yt-dlp-gui/blob/master/image.jpg)
## Required:
To run the program, you need python itself and the installed PyQt5 module and of course you need [yt-dlp](https://github.com/yt-dlp/yt-dlp) for this to work.

###Attention! The program was written and tested on Linux

## Installing python and PyQt5 modules.  

### MS Windows:
You can download the distribution from [python.org](https://www.python.org/downloads/) and double-click the installation  
after installation, you need to install the `PyQt5`  module, to do this in the console enter 
```console
python -m pip install pyqt5
```
the program will download and install the module.
To run this program, you must enter in the console
```console
python program_path\yt_dlp_gui.py
```
You can also create a launch shortcut on the desktop.
To run from a shortcut, use `pythonw` instead of `python`
```console
pythonw program_path\yt_dlp_gui.py
```

### Linux:
For the program to work in Linux, you need to use python version 3 or higher.
Most distributions have python preinstalled and you don't need to download and install it, 
you just need to install the `PyQt5` module.
If you do not have python3 installed, you can install it using your package manager, 
for example, in distributions based on Debian, it is installed like this:
```console
sudo apt-get install python3
```
To install the module in the console, enter
```console
sudo apt install python3-pyqt5
```

modules will be automatically downloaded and installed.
The program starts like this:
```console
python3 program_path/yt_dlp_gui.py
```
You can also add permission to run the script and double-click to run it, as well as create a desktop shortcut.

Author: Roganov G.V. roganovg@mail.ru


