from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class HotSauceForm(FlaskForm):
    """Form for adding a new hot sauce."""

    name = StringField("Hot Sauce Name", validators=[InputRequired()])
    base = SelectField('Sauce Base',
                       choices=[("vinegar"), ("pepper purée"), ("tomato paste"), ("tomatoes (salsa style)"),
                                ("tomatillo"), ("fruit/vegtable purée"), ("water"), ("chili oil"), ("mustard"),
                                ("fruit juice")])
    pepper = SelectField('Main Pepper Variety',
                         choices=[("jalapeño"), ("habanero"), ("cayenne"), ("chili"), ("scotch bonnet"),
                                  ("guajilla"), ("ghost (bhut jolokia)"), ("serrano"), ("Trinidad scorpion"),
                                  ("fresno"), ("shishito"), ("Carolina reaper"), ("harissa"), ("piri piri chili"),
                                  ("gochujang"), ("poblano"), ("chipotle"), ("capsaicin extract")])
    bottle = SelectField('Bottle Style',
                         choices=[("small bottle red"), ("small bottle green"), ("small bottle orange"),
                                  ("tall bottle"), ("large wide bottle"), ("small jar"), ("wide jar"), ("tub")])


class RateHotSauceForm(FlaskForm):
    """Form for rating an existing hot sauce"""

    hotsauce = SelectField('Hot Sauce', coerce=int)
    flavor = SelectField('Flavor Rating',
                         choices=[("1"), ("2"), ("3"), ("4"), ("5"), ("6"), ("7"), ("8"), ("9"), ("10")])
    heat = SelectField('Hotness Level', choices=[("1"), ("2"), ("3"), ("4"), ("5"), ("6"), ("7"), ("8"), ("9"), ("10")])
