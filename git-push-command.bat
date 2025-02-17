@echo on
REM Activate the virtual environment
call "C:\Users\SynergexSystems\Documents\utilities\github-push-script\.venv\Scripts\activate.bat"

REM Run the Python script
python "C:\Users\SynergexSystems\Documents\utilities\github-push-script\git-push-command.bat"

REM Deactivate the virtual environment
deactivate