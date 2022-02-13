# Python Shell File Downloader

**WIP**

## About

This Python command-line program is supposed to be able to download multiple files using the shell *curl* command.

Runs on Python 3.5 preferably, probably at least Python 3.2

## Use
1. Open shell in macOS or Linux (or a bash compatible shell on Windows such as *MINGW64*)
2. *python3 file_dwld.py* (or *python file_dwld* depending on the symlink)
3. Accept usage of application. If not accepted, quit.
4. Determine download directory
5. Input url and for each file
6. Download the files
7. Ask user if they want to go again. If so, go back to step **3**. Else, quit.

**TODO**
- Display which files have failed to download
- Perhaps make a stronger check for the validity of the url link
- Make it a GUI app (**very big maybe?**)
