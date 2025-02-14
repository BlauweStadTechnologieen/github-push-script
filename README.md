## Installation Packages

#### Python
Download the latest verision of `Python`from https://www.python.org/.
Once downloaded you can confirm that Python, as well as the version, is installed on your system by running the command `py --version`. If you already have a version of Python installed in your system and you're simply upgrading this, you can run `py -x-xx --version` so your system points to the correct version of Python.

#### Git Bash
Download the latest verion of `Git` frm https://git-scm.com/downloads/win

#### MT4 Terminal
You can download the latest version of the MT4 terminal, which will by default come with the MetaEditor4 application.

## Setup

#### Selecting the directories | Pushing to your Remote Directory
Choose which directories you wish to link to your Github, by running `git init`. This will place a folder named `.git` in the directory.

#### Selecting rhe directories | Pulling from your Remote Directory
Alternatively, you can simply run the `git clone <github-remote-repo-address>`. This will automatically initialize the local git repo. 

## Creating a virtual environment
Creating a virtual environment will separate the package versions you will use for your script. If you want to create a virtual environment, this is know as the `.venv`. 
Simply run the following command: `py -m venv .venv`.

The, activate it by running the following command: `.venv\Scripts\activate`


## Creating a variables environment
You can also create a variables environment, referred to as `.env`. You can do this by running the following command: `py` 
