from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    SelectField,
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from admin.models import User, Sensor


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Create User")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already in use.")


class EditUserForm(FlaskForm):
    id = IntegerField("ID")
    username = StringField("Username")
    password = PasswordField("Password")
    password2 = PasswordField("Repeat Password", validators=[EqualTo("password")])
    submit = SubmitField("Edit User")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user and (user.id != self.id.data):
            self.username.errors.append("Username already used by another user")
            return False

        return True


class AddDeviceform(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Save User")


class AddSensorForm(FlaskForm):
    deviceid = IntegerField("Device Id")
    name = StringField("Name", validators=[DataRequired()])
    type = SelectField(
        "Device Type",
        choices=[
            ("", "Please select an option"),
            ("reader", "Reader"),
            ("controller", "Controller"),
        ],
        default=None,
        validators=[DataRequired()],
    )
    submit = SubmitField("Save Sensor")
