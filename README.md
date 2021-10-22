![build](https://github.com/elhusseiniali/flask-alfred/workflows/build/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/elhusseiniali/flask-alfred/badge.svg?branch=master)](https://coveralls.io/github/elhusseiniali/flask-alfred?branch=master)
# flask alfred
CMPS Helper System is a Flask app built to help organize the students requests submitted to a univeristy department.

# Setup:
We recommend using Python 3.6 or newer. You will have to create your own virtual environment pyenv-virtualenv is a great option for that. You will need to install the requirements using pip install -r requirements.txt (use pip3 if you aren't using pyenv).

If this is your first time running the project, you will need to instantiate an empty database using python reset.py.

You can run the app using python run.py. The terminal will show you what address to use to visit the app in a modern browser (usually it is something like localhost:5000/ or localhost:5001/).

You can access the admin panel by going to the /admin path (e.g. localhost:5000/admin). You can access the API doc page by going to the /api/1 path (e.g. localhost:5000/api/1).

For sending emails to work, you will have to add environment variables. The first one is "MAIL_USERNAME" with a value of your full aub email address. The second one is "MAIL_PASSWORD" with a value of your password of aub email.  
