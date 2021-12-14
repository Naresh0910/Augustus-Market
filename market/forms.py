from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired ,ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_user_name(self, user_name_to_check):
        user = User.query.filter_by(user_name=user_name_to_check.data).first()
        if user:
            raise ValidationError('username already exits!please try different username')

    def validate_email(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exits!please try different email')


    user_name = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[DataRequired(),Email()])
    password1 = PasswordField(label='*Enter Password', validators=[Length(min=4), DataRequired()])
    password2 = PasswordField(label='*Re-Enter Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):

    user_name = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign-in')


class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label='purchase item!')

class SellItemForm(FlaskForm):
    submit=SubmitField(label='sell item!')