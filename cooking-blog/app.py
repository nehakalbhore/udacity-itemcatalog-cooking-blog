#!/usr/bin/env python
import datetime
import httplib2
import json
import random
import requests
import string
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db import (Base, Users, Cuisine, Recipe)
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   make_response,
                   flash,
                   jsonify,
                   session)

from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth(scheme='Token')

app = Flask(__name__)
app.secret_key = 'super_secret_key'

GOOGLE_CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
    'web']['client_id']

# Connect to Database and create database session
engine = create_engine(
    'sqlite:///rb.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session_db = DBSession()

memory = []
currentUser = None


@auth.verify_token
def verify_token(token):
    access_token = session.get('access_token')
    return access_token is not None


def cuisine_check(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if request.endpoint == 'index':
            kwargs['cuisine'] = 'all'
        elif 'cuisine' in kwargs and kwargs['cuisine'].lower() != 'all':
            kwargs['cuisine'] = kwargs['cuisine'].title()
            cuisineExists = session_db.query(Cuisine.id)\
                .filter_by(name=kwargs['cuisine'])\
                .scalar() is not None
            if not cuisineExists:
                response = make_response(
                    json.dumps('Resource not found.'), 404)
                response.headers['Content-Type'] = 'application/json'
                return response
        return func(*args, **kwargs)
    return wrap


def add_cuisines(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        kwargs['cuisine_entries'] = session_db.query(Cuisine).all()
        return func(*args, **kwargs)
    return wrap


def add_recipe(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        recipe = session_db.query(Recipe)\
            .join(Recipe.cuisine)\
            .join(Recipe.user)\
            .filter(Recipe.id == kwargs['recipe_id'])\
            .one_or_none()

        if recipe:
            kwargs['recipe'] = recipe
        else:
            response = make_response(json.dumps('Resource not found.'), 404)
            response.headers['Content-Type'] = 'application/json'
            return response
        return func(*args, **kwargs)
    return wrap


def owner_check(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        recipe = kwargs.get('recipe')
        email = session.get('email')
        if recipe is None:
            response = make_response(json.dumps('Recipe not found.'), 404)
            response.headers['Content-Type'] = 'application/json'
            return response
        elif email is None:
            response = make_response(json.dumps(
                'Modification not allowed. You are not signed in.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        elif recipe.user.email != email:
            response = make_response(json.dumps('Unauthorized.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        return func(*args, **kwargs)
    return wrap


@app.route('/', endpoint='index', methods=['GET', 'POST'])
@app.route('/cuisine/<cuisine>/', endpoint='show-cuisine',
           methods=['GET', 'POST'])
@cuisine_check
@add_cuisines
def index(cuisine, cuisine_entries):
    if request.method == 'GET':
        recipes = []
        query = session_db.query(Recipe)\
            .join(Recipe.cuisine)\
            .order_by(asc(Recipe.created))
        if cuisine == 'all':
            recipes = query.all()
        else:
            recipes = query.filter(Cuisine.name == cuisine).all()

        user = session.get('username', None)
        return render_template('layout.html',
                               index=True,
                               cuisine_entries=cuisine_entries,
                               this_cuisine=cuisine,
                               recipes=recipes,
                               user=user)
    elif request.method == 'POST' and 'recipe' in request.form:
        cuisine_name = cuisine
        if cuisine_name.lower() == 'all':
            cuisine_name = 'no-cuisine'

        cuisine_entry = session_db.query(cuisines)\
            .filter_by(name=cuisine_name)\
            .one()

        user_id = None
        email = session.get('email')
        if email:
            user = session_db.query(Users)\
                .filter_by(email=email)\
                .first()
            if user:
                user_id = user.id
        recipe = Recipe(body=request.form['recipe'],
                        created=datetime.datetime.now(),
                        cuisine_id=cuisine_entry.id,
                        user_id=user_id or 1)
        session_db.add(recipe)
        session_db.commit()
        return redirect(url_for('show-cuisine', cuisine=cuisine))


@app.route('/cuisine/<cuisine>/recipe/<int:recipe_id>')
@cuisine_check
def showRecipe(cuisine, recipe_id):
    recipe = session_db.query(Recipe)\
        .join(Recipe.cuisine)\
        .join(Recipe.user)\
        .filter(Recipe.id == recipe_id)\
        .one_or_none()

    if recipe is None:
        response = make_response(json.dumps('Resource not found.'), 404)
        response.headers['Content-Type'] = 'application/json'
        return response

    canModify = False
    email = session.get('email')
    if email is not None and recipe.user.email == email:
        canModify = True

    user = session.get('username')
    return render_template(
        'layout.html',
        user=user,
        show_recipe=True,
        recipe=recipe,
        modification_allowed=canModify
    )


@app.route('/cuisine/<cuisine>/recipe/<int:recipe_id>/delete/',
           methods=['POST'])
@auth.login_required
@cuisine_check
@add_recipe
@owner_check
def deleteRecipe(cuisine, recipe_id, recipe):
    """ Delete recipe endpoint to delete given recipe. In order to
    execute this endpoint, user must be logged in.
    """
    session_db.delete(recipe)
    session_db.commit()
    flash('Recipe has been deleted')
    return redirect(url_for('index'))


@app.route('/cuisine/<cuisine>/recipe/<int:recipe_id>/edit/',
           methods=['GET', 'POST'])
@auth.login_required
@cuisine_check
@add_recipe
@owner_check
def editRecipe(cuisine, recipe_id, recipe):
    """ Edit recipe endpoint to edit an existing recipe. In order to
    execute this endpoint, user must be logged in.
    """
    if request.method == 'GET':
        user = session.get('username')
        return render_template(
            'layout.html',
            edit_recipe=True,
            user=user,
            recipe=recipe,
            cuisine=cuisine)

    if request.method == 'POST' and 'recipe' in request.form:
        recipe.body = request.form['recipe']
        recipe.ingredients = request.form['ingredients']
        session_db.add(recipe)
        session_db.commit()
        flash('Recipe has been updated')
        return redirect(url_for('index'))


@app.route('/recipe/new/', methods=['GET', 'POST'])
@auth.login_required
@add_cuisines
def newRecipe(cuisine_entries):
    """This endpoint adds a new recipe into database. In order to
    execute this endpoint, user must be logged in.
    """
    if request.method == 'GET':
        user = session.get('username', None)
        return render_template(
            'layout.html',
            user=user,
            new_recipe=True,
            cuisines=cuisine_entries)

    if request.method == 'POST' and 'recipe' in request.form:
        email = session.get('email', None)
        cuisine_name = request.form['cuisine']
        cuisine = session_db.query(Cuisine).filter_by(
            name=cuisine_name).one_or_none()
        user = session_db.query(Users).filter_by(email=email).one_or_none()

        recipe = Recipe(
            name=request.form['name'],
            cuisine_id=cuisine.id,
            ingredients=request.form['ingredients'],
            body=request.form['recipe'],
            user_id=user.id,
            created=datetime.datetime.now()
        )

        session_db.add(recipe)
        session_db.commit()
        flash('Recipe has been created')
        return redirect(url_for('index'))


@app.route('/api/v1/cuisines')
@add_cuisines
def showcuisinesAPI(cuisine_entries):
    cuisines = [entry.serialize for entry in cuisine_entries]
    return jsonify(cuisines=cuisines)


@app.route('/api/v1/cuisines/<cuisine>')
@cuisine_check
def showcuisineAPI(cuisine):
    entries = session_db.query(Recipe)\
        .join(Recipe.cuisine)\
        .order_by(asc(Recipe.created))\
        .filter(Cuisine.name == cuisine)\
        .all()
    recipes = [entry.serialize for entry in entries]
    return jsonify(recipes=recipes)


@app.route('/api/v1/cuisines/<cuisine>/recipe/<int:recipe_id>')
@cuisine_check
@add_recipe
def showRecipeAPI(cuisine, recipe_id, recipe):
    return jsonify(recipe=recipe.serialize)


@app.route('/signin')
def showLogin():
    """ Sign in user useing google API"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template('signin.html', state=state,
                           GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ gconnect handles the google signin process on the server side."""
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_google_id = session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    session['access_token'] = credentials.access_token
    session['google_id'] = google_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    session['logged_in'] = True
    session['provider'] = 'google'
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    user = session_db.query(Users)\
        .filter_by(email=data['email'])\
        .first()
    if not user:
        user = Users(name=data['name'], email=data['email'])
        session_db.add(user)
        session_db.commit()

    msg = "You are now logged in as %s"
    flash(msg % session['username'])

    return render_template('login-success.html',
                           username=session['username'],
                           img_url=session['picture'])


@app.route('/sign-out')
def signOut():
    access_token = None
    if 'access_token' in session:
        access_token = session['access_token']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    del session['logged_in']
    del session['access_token']
    del session['google_id']
    del session['username']
    del session['email']
    del session['picture']
    del session['provider']
    flash("You have been logged out")
    return render_template('signout.html', GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
