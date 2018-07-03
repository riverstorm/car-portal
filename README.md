# Car Market

<b>This flask application shows a simple website to list cars for sale.</b><br>
It offers features to create, edit and delete offers, secured by Google Auth. Listed offers are readable for the public.
### An Udacity Project
The project is part of my Udacity course and uses some provided resources.
<br><br>
<b>The requirements are exceeded by at least the following features or changes:</b>
<br>
* Image handling
* CSRF protection

## Installation
### Requirements
* A Windows, Mac or Linux machine with Python 3
* The Python library [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org) and [Flask-Migrate](https://flask-migrate.readthedocs.io). Simply run `pip install -r requirements.txt` to install the libraries.
* A client_secrets.json file from your [Google Auth](https://developers.google.com/identity/) account. Place this file in the root directory, next to your app.py file.

### Instruction
1. In a terminal of your choice, switch to the directory that contains the app.py file. In this repository it would be the /src directory.
1. Execute the command `export FLASK_APP=app.py` on a Unix system or `set FLASK_APP=app.py` on Windows. This tells the terminal what application it should work with or what file contains the main flask application.
1. Set up the database by executing the commands `flask db init`, `flask db migrate` and finally `flask db upgrade`.
1. The app setup is completed now. Start the app with the command `flask run` or `flask run --host=0.0.0.0` if you are using a development environment like vagrant. The app should now be reachable at [localhost:5000](http://localhost:5000) in your browser.
1. You should start by adding categories. Therefor give yourself admin permissions by opening /admin in your website, copy your personal Google ID and include it in the app.py file. If you are not in debug mode, restart your Flask application.

## Additional informations
### Permission settings
* Offers can be added by all authorized users and viewed by not authorized users.
* Go to "my offers" to edit or delete your own offers

### Usage of this application
This project was built to show a wider range of functionality but <b>not to be used in production</b> or to provide a real "online car market".
