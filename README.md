## Installation Packages

#### Python
Download the latest verision of `Python`from https://www.python.org/.
Once downloaded you can confirm that Python, as well as the version, is installed on your system by running the command `py --version`. If you already have a version of Python installed in your system and you're simply upgrading this, you can run `py -x.xx --version` so your system points to the correct version of Python.

#### Git Bash
Download the latest verion of `Git` frm https://git-scm.com/downloads/win

#### MT4 Terminal
You can download the latest version of the MT4 terminal, which will by default come with the MetaEditor4 application.

## Setup
Nagivate to the correct location where you would like your script to be located, and run the following command:
```
git clone git@github.com:BlauweStadTechnologieen/github-push-script.git
```
#### Creating a variables environment
You can also create a variables environment, referred to as `.env`, short for "environment variables". 

Create a file by running the following command:
```
mkdir .env
```
You will then need to install the `python-dotenv` module in the folling fashion:
```
pip install python-dotenv
```
[-] This should be included in the `requirements.txt` file.

#### Use Case:
Creating a `.env` file which will be used to contain sensitive data:
```
#.env
API_KEY=your_api_key
DATABASE_URL=your_database_url
DEBUG=True
```
You can then include the following into your `git-commit.py` script
```
#git-commit.py

from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env
api_key = os.getenv("API_KEY")

#### Creating a virtual environment
Creating a virtual environment will separate the package versions you will use for your script and will prevent any clashing of other scripts or projects which may be using differeing versions of the same packages.

If you want to create a virtual environment, this is known usually referred to as `.venv`. 

Simply run the following command:
```
py -m venv .venv
```
Then activate it by running the following command: 
```
.venv\Scripts\activate
```
## Installing the dependancies
Your script will have a list of dependancies which it will need to operate smoothly. 

Run the following command:
```
pip install -r requirements.txt
```
#### Testing Git Commit script
Navigate to the correct directory and run the following command:
```
git pull
```
This will just ensure that you have the latest upgrade of the script. 

Aftwerwards, run the following command:
```
git-commit.py
```
You should see a log of directories with which have been committed to the remote repository. If you have any errors, you will receive a GUID reference number, as well as a helpdesk ticket where you can add any further information if you see fit.

#### Creating a .BAT file
The `.BAT`file will activate the `.venv` when triggered by the Windows Task Scheduler application, it will then run the script, before deactivating the virtual environment once the script has finished running.

```
#git-commit.BAT

@echo off
REM Activate the virtual environment
call C:\path\to\your\virtualenv\Scripts\activate.bat

REM Run the Python script
python C:\path\to\your\git-commit.py

REM Deactivate the virtual environment
deactivate
```

