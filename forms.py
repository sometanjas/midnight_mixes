# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    email = StringField(
        'E-Mail',
        validators=[
            DataRequired(message="E-Mail ist erforderlich"),
            Email(message="Ungültiges E-Mail-Format"),
            Length(max=120)
        ]
    )
    password = PasswordField(
        'Passwort',
        validators=[
            DataRequired(message="Passwort ist erforderlich"),
            Length(min=6, message="Passwort muss mind. 6 Zeichen lang sein")
        ]
    )
    confirm_password = PasswordField(
        'Passwort bestätigen',
        validators=[
            DataRequired(message="Bitte Passwort bestätigen"),
            EqualTo('password', message="Passwörter müssen übereinstimmen")
        ]
    )
    submit = SubmitField('CREATE ACCOUNT')


class LoginForm(FlaskForm):
    email = StringField(
        'E-Mail',
        validators=[
            DataRequired(message="E-Mail ist erforderlich"),
            Email(message="Ungültiges E-Mail-Format"),
            Length(max=120)
        ]
    )
    password = PasswordField(
        'Passwort',
        validators=[DataRequired(message="Passwort ist erforderlich")]
    )
    submit = SubmitField('LOG IN')


class IngredientSearchForm(FlaskForm):
    item = StringField('Search by Ingredient', validators=[DataRequired()])
    submit = SubmitField('Search')
