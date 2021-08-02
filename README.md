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

3. Create a virtual enviroment: (OPTIONAL but recommended)
```bash
python -m venv env
```

If you don't have python virtual enviroment installed, then install using:
```bash
pip install virtualenv
```

4. Activate virtual enviroment: (Only needed if you created venv)
```bash
.\env\Scripts\activate.ps1
```

5. Install required packages:
```bash
pip install -r .\requirements.txt
```

6. Rename enviroment variables file:
```bash
cp .env.example .env
```

7. Change variables in .env file: ***IMPORTANT!***
```
WEBHALLEN_USERNAME="example_email"        # Set your login email
WEBHALLEN_PASSWORD="example_password"     # Set your login password
WEBHALLEN_USER_ID="example_id"            # Set your User ID (optional)
VERBOSE="False"                           # Prints sensitive data in the terminal
DEBUG="False"                             # Run program fully regardless of responses from Webhallen
CONTINUOUS="False"                        # Continuously run script and grab supply every midnight
``` 
User ID can be found when logged into Webhallen, example:
`https://www.webhallen.com/se/member/`**`123456`**`/orders`
Otherwise script grabs it from cookies automatically :)

8. Remove old one enviroment variable file: (OPTIONAL)
```bash
rm .env.example
```

9. Run script!
```bash
python .\AdiliusWSDG.py
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

Contact me at Smokey#4150 for inquiries

## Acknowledgment

Acknowledgement to [mirague](https://github.com/mirague) with their [webhallen-supply-drop](https://github.com/mirague/webhallen-supply-drop) repository which sparked the idea for this python project.

https://github.com/mirague/webhallen-supply-drop

## License
[MIT](https://github.com/Adilius/AdiliusWSDG/blob/master/LICENSE)

