<div align="center">

![large_2](https://user-images.githubusercontent.com/43440295/153767327-512a4741-143e-4720-90a7-c603393aba13.png)
 
</div>
 
# AdiliusWSDG: Automate your webhallen experience with Python!

AdiliusWSDG is a simple local Python script to automatically grab supply drops (weekly, activity, level up) for your account.
Its goal is to enchance the Webhallen experience for the tech enthusiast.
With an easy one-time setup never again miss a supply drop.
More features to come!

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
|-v --verbose| Increase verbose levels: <br/>0. No verbosity (default) <br/>1. Prints & logs more debug messages <br/>2. Account details included (email & password) |


## Enviroment variables (optional)

At first run, or if enviroment file is missing/corrupt. You will be prompted for variables to run the script.
| Variable name | Value | Description |
| :---         |     :---:      |         :---  |
|WEBHALLEN_USERNAME| example_email     | Set your login email    |
|WEBHALLEN_PASSWORD| example_password     | Set your login password    |
| SAVE_ENV   | y/n    | Save enviroment variables for next future executions    |

## Setting up scheduled task
TODO
Cron in linux, scheduler in windows

## Run continiously
The script can be setup to run in the background as a continuous process.

### Windows
1. Run script to initialize variables: `python .\adiliuswsdg.py`
2. Create a new minimized command prompt: `cmd.exe /c start /min python .\adiliuswsdg.py -c`

### Linux
1. Run script to initialize variables: `python3 .\adiliuswsdg.py`
2. Start a new "no hang up" process in the background: `nohup python3 adiliuswsdg.py -c &`

Killing the process can easily be done by using: `pkill -9 -f adiliuswsdg`

## Contributing

If you experiance any problems running the script, make an issue.

If you want to contribute, make a pull request.

## Acknowledgment

Acknowledgement to [mirague](https://github.com/mirague) with their [webhallen-supply-drop](https://github.com/mirague/webhallen-supply-drop) repository which sparked the idea for this python project.
