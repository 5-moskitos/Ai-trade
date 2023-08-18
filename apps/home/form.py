from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError

class AddMoney(FlaskForm):
    moneytoadd = StringField('MoneytoAdd',
                         id='moneytoadd',
                         validators=[DataRequired()])

class WithdrawMoney(FlaskForm):
    moneytowith = StringField('MoneytoWithdraw', id='moneytowith', validators=[DataRequired()])