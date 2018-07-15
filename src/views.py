"""
The views.py file includes all GET and POST operations of the application.
"""
from app import app, db
from app import CLIENT_ID
from models import Category, Item
import flask
import os
import random
import string
import httplib2
import json
import requests
from flask import Flask, render_template, request, flash, make_response, \
    redirect, jsonify
from flask import session as login_session
from werkzeug.utils import secure_filename
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from functions import validate_csrf_get, validate_csrf_post, login_required, \
    admin


# Displays an overview of all available offers
@app.route("/")
def offer_overview():
    items = Item.query.order_by(Item.date.desc())
    categories = Category.query
    return render_template('offer_overview.html', cars=items,
                           categories=categories)


# Displays an overview of all available offers
@app.route("/<category>")
def offer_overview_category(category):
    items = Item.query.filter_by(category=category)
    categories = Category.query
    return render_template('offer_overview.html', cars=items,
                           categories=categories)


# Displays an overview of all available offers as JSON
@app.route("/json")
def offer_overview_json():
    items = Item.query.order_by(Item.date.desc())
    return jsonify(Offers=[x.serialize for x in items])


# Displays or executes a form to create a new offer
@app.route("/cars/create", methods=['GET', 'POST'])
@login_required
@validate_csrf_post
def offer_create():
    """
    Handles the creation of new Items. Items are shown
    as car offers for the public.
    
    Methods:
        GET: If a GET request is made, the offer_create.html template with a
        form is rendered.
        POST: A POST request usually happens on form submit and finally creates
        a new Item object.

    Returns:
        GET method: offer_create.html with a form to execute a POST request.
        POST method: Redirects to homepage with a message in case of success.

    """
    if flask.request.method == 'POST':
        name = request.form['item_name']
        description = request.form['item_description']
        category = request.form['item_category']
        price = request.form['item_price']
        photo = request.files['item_photo']
        year = request.form['item_year']
        fuel = request.form['item_fuel']
        consumption = request.form['item_consumption']
        color = request.form['item_color']
        miles = request.form['item_miles']
        user = login_session['gplus_id']

        filename = secure_filename(photo.filename)

        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        item = Item(name=name, description=description, category=category,
                    price=price, photo=filename, year=year, fuel=fuel,
                    consumption=consumption, color=color, miles=miles,
                    user=user)
        db.session.add(item)
        db.session.commit()

        flash('Added your offer successfully', 'success')
        return redirect('/')

    else:
        categories = Category.query
        return render_template('offer_create.html', categories=categories)


# Displays the detail page of a single offer
@app.route("/cars/view/<int:car_id>/")
def offer(car_id):
    result = Item.query.filter_by(id=car_id).first()
    return render_template('item.html', car=result)


# Displays the details of a single offer as JSON
@app.route("/cars/view/<int:car_id>/json")
def offer_json(car_id):
    result = Item.query.filter_by(id=car_id).first()
    return jsonify(result.serialize)


# Displays an overview of all offers that are owned by the current user
@app.route("/myoffers/overview")
@login_required
def offer_user():
    result = Item.query.filter_by(user=login_session['gplus_id'])
    return render_template('offer_user.html', cars=result)


# Displays an overview of all available categories
@app.route("/categories/overview")
def category_overview():
    result = Category.query
    return render_template('overview_categories.html', categories=result)


# Displays or executes a form to create a new category
@app.route("/categories/create", methods=['GET', 'POST'])
@login_required
@admin
@validate_csrf_post
def category_create():
    """
    Handles the creation of new Categories.

    Notes:
        Requires admin permission.
    
    Methods:
        GET: If a GET request is made, the category_create.html template with a
        form is rendered.
        POST: A POST request usually happens on form submit and creates a new
        Category object.

    Returns:
        GET method: category_create.html with a form.
        POST method: category_create.html with a form and a success message.

    """
    if flask.request.method == 'POST':
        name = request.form['category_name']
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

        flash('You created the category successfully', 'success')
        return render_template('category_create.html')

    else:
        return render_template('category_create.html')


# Displays or executes a form to edit an offer
@app.route("/cars/edit/<int:car_id>/", methods=['GET', 'POST'])
def offer_edit(car_id):
    """
    Handles the editing of existing Items.
    
    Methods:
        GET: If a GET request is made, the offer_edit.html template with a form
        is rendered. The form includes current values.
        POST: A POST request that happens on form submit updates the existing
        items with the form values.

    Parameters:
        car_id: The primary and unique id of the Item to be edited

    Returns:
        GET method: offer_edit.html with a prefilled form to execute a POST
        request.
        POST method: Redirects to homepage with a message in case of success.

    """
    if flask.request.method == 'POST':
        result = Item.query.filter_by(id=car_id).first()
        result.name = request.form['item_name']
        result.description = request.form['item_description']
        result.category = request.form['item_category']
        result.price = request.form['item_price']
        result.year = request.form['item_year']
        result.fuel = request.form['item_fuel']
        result.consumption = request.form['item_consumption']
        result.color = request.form['item_color']
        result.miles = request.form['item_miles']
        result.user = login_session['gplus_id']
        if request.files:
            photo = request.files['item_photo']
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result.photo = filename

        db.session.commit()

        flash('Edited your offer successfully', 'success')
        return redirect('/')
    else:
        result = Item.query.filter_by(id=car_id).first()
        return render_template('offer_edit.html', car=result)


# Displays or executes a form to delete an offer
@app.route("/cars/delete/<int:car_id>/", methods=['GET', 'POST'])
@login_required
@validate_csrf_post
def offer_delete(car_id):
    """
    Handles the deletion of existing Items. Only the owner of the Item is able
    to delete it. The owner is verified by a comparison with the login sessions
    user id.
    
    Methods:
        GET: The GET request shows a form as a simple button to retrieve
        verification of Item deletion.
        POST: A POST request deleted the requested Item.

    Parameters:
        car_id: The primary and unique id of the Item to be deleted.

    Returns:
        GET method: offer_delete.html with form button or a redirect to the
        homepage with an error message if the Items owner does not match.
        POST method: Redirects to homepage with a success message or with an
        error message if the Items owner does not match.

    """
    item = Item.query.filter_by(id=car_id).first()
    if login_session['gplus_id'] == item.user:
        if flask.request.method == 'POST':
            db.session.delete(item)
            db.session.commit()
            flash('Item ' + str(item.id) + ' successfully deleted', 'success')
            return redirect('/')
        else:
            result = Item.query.filter_by(id=car_id).first()
            return render_template('offer_delete.html', car=result)
    else:
        flash('This is not your offer', 'error')
        return redirect('/')


# Displays the login page
@app.route("/login")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Executes the login with google plus
@app.route('/gconnect', methods=['POST'])
@validate_csrf_get
def gconnect():
    """
    Handles the login of a user by connecting with Google Plus.
    
    Methods:
        POST: Receives the request from the 'login' functions form

    Returns:
        Returns 'success' in case the login was successful.
        The user is redirected to the homepage by using Javascript and receives
        a flash success message.

    """
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(request.data)
    except FlowExchangeError:
        response = make_response(
            json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already connected.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token and gplus id in sessions.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Retrieve user information.
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store user information in sessions.
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = 'success'
    flash('You are now logged in as %s' % login_session['username'], 'success')

    return output


# Log the current user out of the page / disconnect from google plus
@app.route('/logout')
def logout():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps("Current user not connected."), 
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers['Content-Type'] = 'application/json'

        flash('Successfully logged out', 'success')
        return redirect('/login')
    else:
        response = make_response(
            json.dumps("Failed to revoke token for given user.", 400))
        response.headers['Content-Type'] = 'application/json'
        return response
