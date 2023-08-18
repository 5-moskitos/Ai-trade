# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    phone_no = StringField('Phone_Number',id='Phone_Number', validators=[DataRequired()])
    current_balance= StringField('current_balance', id='current_balance')
    
class Transaction(FlaskForm):
    transaction_id=StringField('tran_id',id='tran_id',validators=[DataRequired()])
    date_time =  StringField('dateTime', id='date_time', validators=[DataRequired()])
    Stock_name = StringField('Stock_Name', id='stockname', validators=[DataRequired()])
    buySell = StringField('BuySell',id='buysell', validators=[DataRequired()])
    Price = StringField('price',id='price',validators=[DataRequired()])
    quantity= StringField('quantity',id='quantity',validators=[DataRequired()]) 

    