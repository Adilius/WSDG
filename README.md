<div align="center">
 
![large_2](https://user-images.githubusercontent.com/43440295/153767327-512a4741-143e-4720-90a7-c603393aba13.png)

# AdiliusWSDG 
</div>

![Python version](https://img.shields.io/badge/python-v3.9.6-blue)

Simple local Python script to get status of supply drops (weekly/daily, activity, level up) and grab them for your account automatically.

![RUNTIME](https://user-images.githubusercontent.com/43440295/127823499-2a855c8f-ba7d-4f6b-b3aa-0a05f862e04a.gif)

![LOGS](https://user-images.githubusercontent.com/43440295/134048866-0243ae2a-23a8-432a-acc8-a8d3ec1af201.png)


## Quick start
1. Clone repository: `git clone https://github.com/Adilius/AdiliusWSDG.git`

2. Change directory to repository: `cd AdiliusWSDG/`

3. Install required packages: `pip install -r .\requirements.txt`

4. Run script: `python .\AdiliusWSDG.py`

## Variables

At first run, or if enviroment file is missing/corrupt. You will be prompted for variables to run the script.
| Variable name | Value | Description |
| :---         |     :---:      |         :---  |
|WEBHALLEN_USERNAME| example_email     | Set your login email    |
|WEBHALLEN_PASSWORD| example_password     | Set your login password    |
| VERBOSE   | y/n     | Prints email & password in the terminal (for debugging)    |
| CONTINUOUS   | y/n     | Continuously run script and grab supply every midnight    |
| SAVE_ENV   | y/n    | Save enviroment variables for next future executions    |

## Contributing

If you experiance any problems running the script, make an issue.

If you want to contribute, make a pull request.

## Acknowledgment

Acknowledgement to [mirague](https://github.com/mirague) with their [webhallen-supply-drop](https://github.com/mirague/webhallen-supply-drop) repository which sparked the idea for this python project.

## License
[MIT](https://github.com/Adilius/AdiliusWSDG/blob/master/LICENSE)
