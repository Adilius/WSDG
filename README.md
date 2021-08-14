![Python version](https://img.shields.io/badge/python-v3.9.6-blue)

# AdiliusWSDG - Adilius Webhallen Supply Drop Grabber
Simple local Python script to get status of supply drops (weekly/daily, activity, level up) and grab them for your account automatically.

![AdiliusWSDG](https://user-images.githubusercontent.com/43440295/127823499-2a855c8f-ba7d-4f6b-b3aa-0a05f862e04a.gif)

## Quick start
1. Clone repository:
```bash
git clone https://github.com/Adilius/AdiliusWSDG.git
```
***OR***
```bash
git clone git@github.com:Adilius/AdiliusWSDG.git
```

2. Change directory to repository:
```bash
cd AdiliusWSDG/
```

3. Install required packages:
```bash
pip install -r .\requirements.txt
```

4. Run script!
```bash
python .\AdiliusWSDG.py
```

## Variables

At first prompt, or if enviroment file is missing. You will be prompted for variables
```
WEBHALLEN_USERNAME="example@email.com"        # Set your login email
WEBHALLEN_PASSWORD="example_password"         # Set your login password
VERBOSE="False"                               # Prints sensitive data in the terminal
CONTINUOUS="False"                            # Continuously run script and grab supply every midnight
``` 

## Roadmap

This project is still in early development, things to improve:
- [ ] Cron setup
- [ ] Logging
- [ ] Improved error handling
- [ ] Continious execution with pseudo-random timed actions
- [ ] Header setup/clean-up

## Contributing

If you experiance any problems running the script, make an issue.

If you want to contribute, make a pull request.

## Acknowledgment

Acknowledgement to [mirague](https://github.com/mirague) with their [webhallen-supply-drop](https://github.com/mirague/webhallen-supply-drop) repository which sparked the idea for this python project.

https://github.com/mirague/webhallen-supply-drop

## License
[MIT](https://github.com/Adilius/AdiliusWSDG/blob/master/LICENSE)
