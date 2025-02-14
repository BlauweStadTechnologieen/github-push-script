## Installation Packages

#### Python
Download the latest verision of `Python`from https://www.python.org/.
Once downloaded you can confirm that Python, as well as the version, is installed on your system by running the command `py --version`. If you already have a version of Python installed in your system and you're simply upgrading this, you can run `py -x.xx --version` so your system points to the correct version of Python.

#### Git Bash
Download the latest verion of `Git` frm https://git-scm.com/downloads/win

#### MT4 Terminal
You can download the latest version of the MT4 terminal, which will by default come with the MetaEditor4 application.

## Setup

#### Nagivate to the correct location as to where you script is located

#### Selecting the directories | Pushing to your Remote Directory
Navitate to each directory with which you would like to initialise a local repository, and run the following command:
```
git init
```
#### Selecting rhe directories | Pulling from your Remote Directory
Alternatively, you can simply run the `git clone <github-remote-repo-address>`. This will automatically initialize the local git repo. 

## Creating a virtual environment
Creating a virtual environment will separate the package versions you will use for your script and will prevent clasing of other using which may be using differeing versions of the same packages.

If you want to create a virtual environment, this is known usually referred to as `.venv`. 

Navigate to the relavant directory & simply run the following command:
```
py -m venv .venv
```
Then activate it by running the following command: 
```
.venv\Scripts\activate
```
### Installing the dependancies
Your script will have a list of dependancies which it will need to operate smoothly. 

Run the following command:
```
pip install -r requirements.txt
```
## Creating a variables environment
You can also create a variables environment, referred to as `.env`, short for "environment variables". You can do this by running the following command:
```
pip install python-dotenv
```
[-] This should be included in the `requirements.txt` file.

## Use Case:
Creating a `.env` file which will be used to contain sensitive data:
```
#.env
API_KEY=your_api_key
DATABASE_URL=your_database_url
DEBUG=True
```
Install the `dotenv` module in the following fashion:
```
pip install python-dotenv
```
You can then create a script `script.py` and import the `dotenv` module.
```
#script.py

from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env
api_key = os.getenv("API_KEY")
```
## Testing Git Commit script

Navigate to the correct directory and run the following command:
```
git pull
```
This will just ensure that you have the latest upgrade of the script. 

Once you have completed this, run the following command:
```
git-commit.py
```
You should see a log of directories with which have been committed to the remote repository. If you have any errors, you will receive a GUID reference number, as well as a helpdesk ticket where you can add any further information if you see fit.

#### Creating a .BAT file
The `.BAT`file will activate the `.venv` when triggered by the Windows Task Scheduler application, it will then run the script, before deactivating the virtual environment once the script is finished running.

Create a `.BAT` file in the following fashion:
```
@echo off
REM Activate the virtual environment
call C:\path\to\your\virtualenv\Scripts\activate.bat

REM Run the Python script
python C:\path\to\your\git-commit.py

REM Deactivate the virtual environment
deactivate
```

