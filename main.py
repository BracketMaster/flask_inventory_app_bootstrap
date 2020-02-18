from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from wtforms.validators import Required
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from game_store_db import *
User_DB = User
from forms import *
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user 

nav = Nav()
login_manager = LoginManager()
@nav.navigation()
def mynavbar():
    if current_user.is_authenticated:
        return Navbar(
            'Game Store',
            View('Home', 'index'),
            View('Browse Titles', 'browse'),
            View('My Cart', 'view_cart'),
            View('Logout', 'logout'),
        )
    else:
        return Navbar(
            'Game Store',
            View('Login', 'login'),
        )

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return self.id
    
    def __str__(self):
        return self.id


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)
    nav.init_app(app)
    login_manager.init_app(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'

    @app.route('/login/', methods=('GET', 'POST'))
    def login():
        print("CURRENT USER")
        print(current_user)
        print(type(current_user))
        login = Authenticate()
        if login.data['login']:  # to get error messages to the browser
            if query_user(name=login.username.data, password=login.password.data):
                user = User(login.username.data)
                login_user(user)
                flash('Login Successful', 'success')
                return redirect(url_for('index'))
            else:
                flash('Login Failed', 'danger')
        if login.data['register']:  # to get error messages to the browser
            if query_username(name=login.username.data):
                flash('An account with that username already exists!! \
                    Please choose another name', 'danger')
            else:
                add_user(name=login.username.data, password=login.password.data)
                flash('Account Creation Successful!! Proceed to Login.', 'success')
        return render_template('login.html', login=login)

    @login_manager.user_loader
    def load_user(userid):
        return User(userid)

    # handle login failed
    @app.errorhandler(401)
    def page_not_found(e):
        return(redirect(url_for('login')))

    # somewhere to logout
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    #landing page after logging in. The user can
    #add games here.
    @app.route('/', methods=('GET', 'POST'))
    @login_required
    def index():
        form = GameForm()
        if form.validate_on_submit(): 
            data = form.data
            data.pop('submit_button')
            data.pop('csrf_token')
            add_game(**data)
            flash('Game Added', 'info')
        return render_template('index.html', form=form)

    #view all the current games
    @app.route('/browse/', methods=('GET', 'POST'))
    @login_required
    def browse():
        print(current_user)
        apply_filter = ApplyFilter()
        clear_filter = ClearFilter()
        if apply_filter.data['apply_filter']:
            return redirect(url_for('search'))
        if clear_filter.data['clear_filter']:
            return redirect(url_for('browse'))
        table = search_game_db(**request.args)
        return render_template('browse.html', table=table, apply_filter=apply_filter, clear_filter=clear_filter, title="Available Games")

    #user can see games in his or her cart
    @app.route('/view_cart/', methods=('GET', 'POST'))
    @login_required
    def view_cart():
        checkout = Checkout()
        price=current_cart_cost(str(current_user))
        if checkout.data['checkout']:
            record_transaction(str(current_user),price)
            clear_cart(str(current_user))
            flash(f'Checkout Complete. Enjoy your games.','success')
            return redirect(url_for('index'))
        table = build_user_cart_table(str(current_user))
        return render_template('cart.html', table=table, 
            checkout=checkout, title=f"{current_user}'s cart",
            price=price)

    #a user can remove games from the game database
    @app.route('/delete/', methods=('GET', 'POST'))
    @login_required
    def delete():
        delete_game(request.args.get('title'))
        return redirect(url_for('browse'))

    #a user can remove games from his or her cart
    @app.route('/delete_from_cart/', methods=('GET', 'POST'))
    @login_required
    def delete_from_cart():
        title = request.args.get('title')
        delete_from_cart_db(str(current_user),title)
        return redirect(url_for('browse'))

    #a user can add games to his or her cart
    @app.route('/add_to_cart/', methods=('GET', 'POST'))
    @login_required
    def add_to_cart():
        title = request.args.get('title')
        add_to_cart_db(str(current_user),title)
        flash(f'Added \'{title}\' to Cart','success')
        return redirect(url_for('browse'))

    #a user can search through the video game database
    #by specifying different filters for each game property
    @app.route('/search/', methods=('GET', 'POST'))
    @login_required
    def search():
        search_query = SearchForm()

        if search_query.validate_on_submit():
            data = search_query.data
            data.pop('submit_button')
            data.pop('csrf_token')
            return redirect(url_for('browse',**data))

        return render_template('search.html', form=search_query)
    

    return app

if __name__ == '__main__':
    create_app().run()
