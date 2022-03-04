from market import app
from flask import render_template, url_for, redirect, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
import webbrowser

theme = 'default'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', theme=theme)


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    f"congratulations! you have successfully purchased {p_item_object.name} for {p_item_object.price}₹", category='success')
            else:
                flash(
                    f"Unfortunately,you don't have enough money to purchase {p_item_object.name} ", category='danger')

         # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    f"Congratulations! you have successfully unlocked the source code.", category='success')
                if s_item_object.name == 'Pong-Game':
                    return redirect(url_for('pong_game'))
                elif s_item_object.name == 'Snake-Game':
                    return redirect(url_for('snake_game'))
                elif s_item_object.name == 'Hang Man-Game':
                    return redirect(url_for('hangman_game'))
                elif s_item_object.name == 'check password strength':
                    return redirect(url_for('checkpasswordstrength_game'))
                elif s_item_object.name == 'Fidget-Spinner':
                    return redirect(url_for('Fidget_Spinner_game'))
                else:
                    webbrowser.open('https://www.google.com')
            else:
                flash(
                    f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, selling_form=selling_form, owned_items=owned_items, theme=theme)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(user_name=form.user_name.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account created successfully!You are now logged in as : {user_to_create.user_name}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:  # if there are errors in the forms
        for err_msg in form.errors.values():
            if err_msg[0][23:32] == 'password1':
                err_msg = 'Password does not match!!!'
            flash(
                f'There was an unexpected error in the field : {err_msg}', category='danger')
    return render_template('register.html', form=form, theme=theme)


@app.route('/Login', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login_page():

    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            user_name=form.user_name.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'success! you are logged in as : {attempted_user.user_name}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('username and password do not match!please try again',
                  category='danger')

    return render_template('login.html', form=form, theme=theme)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!!', category='info')
    return redirect(url_for('home_page'))


@app.route('/themes2')
def change_doge():
    global theme
    theme = 'doge'
    return redirect(url_for('home_page'))


@app.route('/themes3')
def change_aot():
    global theme
    theme = 'aot'
    return redirect(url_for('home_page'))


@app.route('/theme0')
def change_got():
    global theme
    theme = 'default'
    return redirect(url_for('home_page'))


@app.route('/contact')
def contact_page():
    return render_template('contact.html', theme=theme)


@app.route('/about')
def about_page():
    return render_template('about.html', theme=theme)


@app.route('/referal')
def referal_page():
    return render_template('popup.html')

# routes for game pages


@app.route('/pong-game111')
def pong_game():
    return render_template('pong_game.html')


@app.route('/snake-game111')
def snake_game():
    return render_template('snake_game.html')


@app.route('/hangman-game111')
def hangman_game():
    return render_template('hangman_game.html')


@app.route('/checkpasswordstrength-game111')
def checkpasswordstrength_game():
    return render_template('checkpasswordstrength_game.html')


@app.route('/Fidget-spinner-game111')
def Fidget_Spinner_game():
    return render_template('Fidget_Spinner.html')
