# Car Portal

<b>This flask application shows a simple website to list cars for sale.</b>
<br><br>
It offers features to create, edit and delete offers, secured by Google Auth. Listed offers are readable for the public.
## An Udacity Project
The project is part of my Udacity course and uses some provided resources.
<br><br>
<b>The requirements are exceeded by at least the following features or changes:</b>
<br>
<ul>
  <li>Image handling</li>
  <li>CSRF protection</li>
</ul>

## Installation
### Requirements
<ul>
  <li>A Windows, Mac or Linux machine with Python 3</li>
  <li>The Python library <i>Flask-SQLAlchemy</i> and <i>Flask-Migrate</i>. Simply run "pip install -r requirements.txt" to install the libraries.</li>
  <li>A client_secrets.json file from your Google Auth account. Place this file in the root directory, next to your app.py file.</li>
</ul>

### Instruction
<ol>
  <li>In a terminal / console of your choice, switch to the directory that contains the app.py file and execute the command <i>flask run</i>. The website should now be reachable at <i>localhost:5000</i></li>
  <li>You should start by adding categories. Therefor give yourself admin permissions by opening /admin in your website, copy your personal Google ID and include it in the app.py file. If you are not in debug mode, restart your Flask application.</li>
  <li>Offers can be added by all authorized users and viewed by not authorized users.</li>
  <li>Go to "my offers" to edit or delete your own offers</li>
</ol>

<b>This project was built to show a wider range of functionality but not to be used in production or to provide a real "online car market".</b>

