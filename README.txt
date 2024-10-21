How to run the program

Step 1:
Cloning the repository
Run this command in the folder you wish the project to be in
git clone https://github.com/eggh234/Fall-2024-Practicum.git

Setting up local env
Run this commend to create a venv directory and start a instance
python3 -m venv venv

Activate the local environment
On Windows:
venv\Scripts\activate

On macOS and Linux:
source venv/bin/activate

Your terminal should now show a venv at the beginning

Step 2:
Make an API Key by going to this website, logging in, and creating a new key
https://platform.openai.com/docs/overview

Set up OpenAI API Key
Go to terminal and type
export OPENAI_API_KEY="YOUR_API_KEY_HERE"

This sets an environment variable called OPENAI_API_KEY which stores your key. This is the env variable called by the program to avoid the need to hardcode the value.

Step 3:
Install dependencies

Install pip
On macOS
If you have brew installed, you can use:

brew install python3
pip usually comes with Python installations. Verify with:
pip3 --version

On Windows
If you have Python installed, pip is typically included. You can verify it using:
pip --version

If it's not installed, you can use the following command:
python -m ensurepip --upgrade

After installing pip, install all required imports
requirements.txt shows all required imports to install
Example:
Required dependency Flask

Example command:
pip install Flask

Repeat for all imports below
Flask
matplotlib
numpy
openai
pydub
requests
scipy
textblob

Step 4:
Setting up the project directory

Ensure your project directory is as follows

Main Folder
├── venv/
├── Website/
│   ├── static/
│   │   ├── spectograms/
│   │   └── uploads/
│   ├── templates/
│   │   ├── index.html
│   │   └── results.html
│   └── Backend.py
├── Speeches/
│   └── [Sample audio files for uploading]
└── Text_Transcripts/
    └── [Transcripts will be automatically created here]

Step 5:
Running the program
Go to Backend.py 

In terminal type
python3 Backend.py

Copy & Paste the provied link into browser
Example link: http://127.0.0.1:5000

Step 6:
Upload files and enjoy the results in the web browser
