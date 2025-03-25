# OCMC's File Parser
## Description
So TMC proctors, you like proctoring by sitting on your butt I see. Don't worry we don't judge, we here at OCMC are quite good at butt sitting ourselves. Don't wanna go in and manually parse your scans into individual documents? Don't wanna rename each file? Well worry no more! Thank god for modern technology am I right?
## Library Dependencies
This script uses the following external libraries:
```bash
pdf2image
dynamsoft_barcode_reader_bundle
numpy
```
If you have any trouble using the `dynamsoft_barcode_reader_bundle`, either talk to me (if I'm still here) or go get the API yourself by searching it up on google. They have pretty clear instructions.

### Setting up
Run the following commands in your console before using this script
```bash
python3 -m venv venv
source venv/bin/activate
pip install pdf2image dynamsoft-barcode-reader-bundle numpy
```
Then make sure that you are using the virtual environment that we have set up by using the shortcut `Ctrl + Shift + P` (Windows) or `Cmd + Shift + P` (MacOS) to open Command Palette. Then select `Python: Select Interpreter` and then something like `Python 3.13.2 ('venv')` (your python might have a different version, so just look for the `('venv')` at the end) and you are good to go.
## Usage
### Mark Scheme Setup
Here's a detailed step-by-step instruction on how to use this script. Collect the exam returns, whether they are a bulk submission or wtv doesn't matter. File type? Doesn't matter. Now, toss all of them into `./inPdf/`, and run `file_parser.py` and you're done, all of the files should be neatly parsed by the serial number in the `./outPdf/` folder.  
There will most likely be a `no-barcode-detected.pdf` in the `./outPdf/` folder. Flip through it to see if any pages had a detection failure and manually fix it if you see one. Sorry, this program isn't always 100% error-free, but this kind of errors are pretty rare. Prolly less than 1% in my experience, so don't worry.  
All done? Go mark the exams shoo (ಠ益ಠ) your students are waiting.

## Acknowledgment
Thank you `pyzbar` for being a giant pain. (why no support for ARM64 architecture??? (凸T_T)凸) Thanks to you I had to spend 4 hrs writing this simple script that I could have done in like 30 minutes.
