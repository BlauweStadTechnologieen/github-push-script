## Installation Packages

#### Scope

#### Python
Download the latest verision of `Python`from https://www.python.org/.
Once downloaded you can confirm that Python, as well as the version, is installed on your system by running the command `py --version`. If you already have a version of Python installed in your system and you're simply upgrading this, you can run `py -x.xx --version` so your system points to the correct version of Python.

#### Git Bash
Download the latest verion of `Git` frm https://git-scm.com/downloads/win

#### MT4 Terminal
You can download the latest version of the MT4 terminal, which will by default come with the MetaEditor4 application.

## Setup
Nagivate to the file directory location where you would like your script to be places, then run the following command:
```
git clone git@github.com:BlauweStadTechnologieen/github-push-script.git
```
Assuming you have linked your local machine to our remote repository, the directory should be populated with the relavant files. 

#### Creating a variables environment (.env).
Environmental variables are variables which are confidential information, such as API tokens, keys, and passwords which are not to be included when we deploy an update into Github. This is why you're required to create a separate `env` file, so that this confidentual information is only available on your local machine and not on Github.  

The `SENDER_DOMAIN` constant must be verified by your SMTP provider. The remaining SMTP settings will be determined by your SMTP provider. These constants start with `SMTP-*`

Please be aware that the `SMTP-EMAIL` and the `SENDER-EMAIL` are not the same. The`SENDER-EMAIL` is constructed by the `SENDER-DEPARTMENT` and the `SENDER_DOMAIN` in the forMat `<SENDER_DEPARTMENT>@<SENDER_DOMAIN>. The `SENDER_DEPARTMENT` can also be a `no-reply` or variations thereof if you have not set up a mailbox or if you do not wish to have your clients reply. 

The `SMTP-EMAIL`, on the other hand, is determined by your SMTP provider. 

Please be aware that the `SENDER_DOMAIN` must be verified by your SMTP provder, or you will not receive any emails and you may receive errors. 

You will also have your API data pertaining to your Freshdesk account, directory information, as well as sender and requester information. 

Whilst being in the root of the directory, create a `.env` file by running the following command:
```
echo. > .env
```
Populate this file with the following information:
```
#.env
OWNER=""
GITHUB_TOKEN=""
DIRECTORY_CODE="" 
BASE_DIR=""#C:/Users/<USER>/AppData/Roaming/MetaQuotes/Terminal/{DIRECTORY_CODE}/MQL4"
SENDER_DOMAIN=""
SENDER_NAME=""
SENDER_DEPARTMENT=""
REQUESTER_NAME=""
REQUESTER_EMAIL=""
SMTP_SERVER=""
SMTP_EMAIL=""
SMTP_PASSWORD=""
SMTP_PORT=
FRESHDESK_DOMAIN=""
FRESHDESK_API_KEY=""
```
It's important that you name thie file `.env` as this used the `dotenv` module, and this will already be included in the .gitignore file.

#### Creating a Virtual Environment (.VENV):
Creating a virtual environment will separate the package versions you will use for your script and will prevent any clashing of other scripts or projects which may be using differeing versions of the same packages.

If you want to create a virtual environment, this is known usually referred to as `.venv`. 

Simply run the following command:
```
py -m venv .venv
```
You will not need to activate the virtual environment, as this will be done automaically each time the script runs. The virtual environment is then deactivated when the script completes.

#### Ensuring you have the latest updates.
Navigate to the correct directory and run the following command to confirm that you have the latest packages installed:
```
git pull
```
#### Installing the dependancies
Your script will have a list of dependancies which can be found in the `requirements.txt` file. Normally, you would need to install these dependances by running the `pip install -r requirements.txt` command. 

However, we now have a built-in function which does this for you. 

#### Testing Git Commit script
Aftwerwards, run the following command:
```
git-commit.py
```
You should see a log of directories with which have been committed to the remote repository. If you have any errors, you will receive a GUID reference number, as well as a helpdesk ticket where you can add any further information if you see fit.

#### The .BAT file
You should see a file named:
`git-push-command.BAT`

The `.BAT`file will activate the `.venv` when triggered by the Windows Task Scheduler application, it will then run the script, before deactivating the virtual environment once the script has finished running.

This will be the file with which you will point the Windows Task Scheduler towards. 
```
#git-push-command.BAT
@echo

REM Activate the virtual environment
call "C:\Users\SynergexSystems\Documents\utilities\github-push-script\.venv\Scripts\activate.bat"

REM Run the Python script
python "C:\Users\SynergexSystems\Documents\utilities\github-push-script\git-commit.py"

REM Deactivate the virtual environment
deactivate
```
Then you will navidate to the correct directory, and run the following command:

```
git-push-command.bat
```
## Maintenance
This script will be updated regularly inline with our release schedule. To ensure that you have the latest version, regularly run the `git pull` command. Also, you may check the release logs as well.

## Maintain your .gitignore file

Before commiting any files, please ensure that you add the follwing to the `.gitignore` file in the root directory:

```
# Ignore all folders
*/ 

# Don't ignore .mqh and .ex4 files
!*.mqh
!*.ex4
```

