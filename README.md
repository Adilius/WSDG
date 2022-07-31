<div align="center">

![large_2](https://user-images.githubusercontent.com/43440295/153767327-512a4741-143e-4720-90a7-c603393aba13.png)
 
</div>
 
# AdiliusWSDG: Automate your webhallen experience with Python!

AdiliusWSDG is a simple local Python script to automatically grab supply drops (weekly, activity, level up) for your account.  
The goal is to enchance the Webhallen experience for the tech enthusiast.
With an easy one-time setup never again miss a supply drop.  

![Python version](https://img.shields.io/badge/python-v3.9.6-blue)


Run-time             |  Logs
:-------------------------:|:-------------------------:
![RUNTIME](https://user-images.githubusercontent.com/43440295/127823499-2a855c8f-ba7d-4f6b-b3aa-0a05f862e04a.gif)  |  ![LOGS](https://user-images.githubusercontent.com/43440295/134048866-0243ae2a-23a8-432a-acc8-a8d3ec1af201.png)



## Quick start
1. Clone repository: `git clone https://github.com/Adilius/AdiliusWSDG.git`

2. Change directory to repository: `cd AdiliusWSDG/`

3. Install required packages: `pip install -r .\requirements.txt`

4. Run script: `python .\adiliuswsdg.py`

## Command Line Arguments

| Command Line Option | Description |
|  :---  |  :---:  |
|-h --help | Show help message and exit |
|-l log_level --log-level log_level| Log level options: ['DEBUGV', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] <br/>DEBUG and below level logs will only be printed in console. <br/>DEBUGV also prints username, password, and userid. |


## Enviroment variables

At first run, or if enviroment file is missing/corrupt. You will be prompted for variables to run the script. 
| Variable name | Value | Description |
| :---         |     :---:      |         :---  |
|WEBHALLEN_USERNAME| example_email     | Set your login email    |
|WEBHALLEN_PASSWORD| example_password     | Set your login password    |
| SAVE_ENV   | y/n    | Save enviroment variables for next future executions    |

## Setting up scheduled task

### Linux
To setup scheduled task in linux simply use crontab jobs.  
To edit cronjobs: `crontab -e`  
Change paths as needed.
```
00 05 * * * cd /path/to/AdiliusWSDG && /usr/bin/python3 adiliuswsdg.py
```

### Windows
Copy paste to notepad.  
Edit paths in $action.  
Execute should path to either your global Python or to the virtual enviroment Python you use for the project.  
Argument should path to adiliuswsdg.py file.
```
$action = New-ScheduledTaskAction -Execute "path\to\python.exe" -Argument "path\to\AdiliusWSDG\adiliuswsdg.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 5:00am
$trigger.StartBoundary = [DateTime]::Parse($trigger.StartBoundary).ToLocalTime().ToString("s")
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName "AdiliusWSDG" -Description "Run AdiliusWSDG script daily"
```

## Contributing

If you experiance any problems running the script, make an issue.  
If you want to contribute, make a pull request.

## Acknowledgment

Acknowledgement to [mirague](https://github.com/mirague) with their [webhallen-supply-drop](https://github.com/mirague/webhallen-supply-drop) repository which sparked the idea for this python project.
