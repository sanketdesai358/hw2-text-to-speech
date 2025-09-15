# HW 2: Text to Speech

## Environment
- Windows 11
- Python 3.10
- Git version 2.51.0
- VS Code with GitHub Copilot

## Steps to Reproduce
1. Open this repo in VS Code
2. Run `git init` to create a .git folder
3. Create a `README.md` to log the enviornment and steps
4. Use `git add` and `git commit` to track changes
5. 2.3: Renamed to 0_tts_test.sh and committed via VS Code Source Control.

## Python environment setup
I created a virtual environment with: 
python -m venv env
source env/Scripts/activate
I then installed the required packages:
python -m pip install --upgrade pip
python -m pip install --upgrade openai "openai[voice_helpers]" sounddevice numpy python-dotenv
I selected this interpreter in VS Code via **Python: Select Interpreter**.

## 3.2 asked us to do a similar portion we did via the scrip
I created a new file named 1_tts_test.py. The script uses the OpenAI Python  to convert text to speech and save then result as an .mp3 file, similar to our shell script
From the terminal (with the virtual environment active) we run:
python 1_tts_test.py

## 3.3 create a new file that plays any text you want
Next we created a file 2_streaming_tts_test.py
Create: narration.txt with whatever text you want to be read
then run python .\2_streaming_tts_test.py which will play this audio on your laptop 

