# AdiliusWSDG - Adilius Webhallen Supply Drop Grabber
Simple local Python script to get status of supply drops (weekly/daily, activity, level up) and grab them for your account automatically.
The source code is barely 300 lines of code, read through it, understand it, and if you want, improve it and make a pull request.

Written in Python 3.9.6

## Quick start
1. Clone repository:
`git clone https://github.com/Adilius/AdiliusWSDG.git`
***OR***
`git clone git@github.com:Adilius/AdiliusWSDG.git`

2. Change directory to repository:
`cd AdiliusWSDG/`

3. Create a virtual enviroment: (OPTIONAL but recommended)
`python -m venv env`
If you don't have python virtual enviroment installed, then install using:
`pip install virtualenv`

4. Activate virtual enviroment: (Only needed if you created venv)
`.\env\Scripts\activate.ps1`

5. Install required packages:
`pip install -r .\requirements.txt`

6. Rename enviroment variables file:
`cp .env.example .env`

7. Change variables in .env file: ***IMPORTANT!***
```
WEBHALLEN_USERNAME="example_email"        # Set your login email
WEBHALLEN_PASSWORD="example_password"     # Set your login password
WEBHALLEN_USER_ID="example_id"            # Set your User ID (optional)
VERBOSE="False"                           # If sensitive data is to be shown in terminal
DEBUG="False"                             # If ignore certain restrictions and run anyways
CONTINUOUS="False"                        # If true, continuously runs script and grabs supply every midnight
``` 
User ID can be found when logged into Webhallen, example:
`https://www.webhallen.com/se/member/123456/orders`
Otherwise script grabs it from cookies automatically :)

8. Remove old one enviroment variable file: (OPTIONAL)
`rm .env.example`

9. Run script!
`python .\AdiliusWSDG.py`

## Call to action
If you experiance any problems running the script, make an issue.

If you want to contribute, make a pull request.

This project is still in early development, things to improve:
- [ ] Cron setup
- [ ] Logging
- [ ] Improved error handling
- [ ] Continious execution with pseudo-random timed actions
- [ ] Header setup/clean-up

Contact me at Smokey#4150
