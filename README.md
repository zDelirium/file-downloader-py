# Python Shell File Downloader

**WIP**

## About

This Python program is supposed to be able to download multiple files using the shell *curl* command.

Developed on Python 3.7.3.

Will decide later on the program flow and features.

Maybe make it a GUI app if I put my mind into it.

## Use
1. Open shell in macOS or Linux (or a bash compatible shell on Windows such as *MINGW64*)
2. *python3 file_dwld.py* or *python file_dwld.py*
3. Accept usage of application. If not accepted, quit.
4. Determine download directory

**TODO**

5. Input file name and url for each file
6. Download the files
7. Ask user if they want to go again. If so, go back to step **3**. Else, quit.

## Some dependencies
- subprocess and os module (should come with python though). But subprocess.run() needs Python 3.5 at least
