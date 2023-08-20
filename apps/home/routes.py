# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, session, redirect, url_for
from flask import render_template, request,session,flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from .utils import get_all_stock_data, make_trade
from .form import AddMoney,WithdrawMoney, TradeForm
from flask_login import current_user
from apps.authentication.models import Users,Transaction
from apps import db


@blueprint.route('/index')
@login_required
def index():
    user_id = session["user_id"]
    username = session["user_name"]
    user = Users.query.filter_by(id=user_id).first()
    tran = Transaction.query.filter_by(uid=user.id).first()
    c=[]
    c.append(tran)
    print(c[0])
    return render_template('home/index.html', segment='index',tran=c)

@blueprint.route('/stocklist/nifty50')
@login_required
def stocklistn50():

    try:
        data = get_all_stock_data("nifty50")
        return render_template("home/" + "stocklist.html", data=data, category="Nifty50")

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print("here ", e)
        return render_template('home/page-500.html'), 500


@blueprint.route('/stocklist/midCap')
@login_required
def stocklistmc():

    try:
        data = get_all_stock_data("midCap")
        return render_template("home/" + "stocklist.html", data=data, category="Mid Cap")

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print("here ", e)
        return render_template('home/page-500.html'), 500



@blueprint.route('/stocklist/smallCap')
@login_required
def stocklistsc():

    try:
        data = get_all_stock_data("smallCap")
        return render_template("home/" + "stocklist.html", data=data, category="Small Cap")

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print("here ", e)
        return render_template('home/page-500.html'), 500

@blueprint.route('/wallet', methods=['POST','GET'])
@login_required
@login_required
def wallet():
    add_money = AddMoney(request.form)
    withdraw_money = WithdrawMoney(request.form)

    if 'moneytoadd' in request.form:
        money = request.form["moneytoadd"]
        user_id = session["user_id"]
        username = session["user_name"]
        print(f"money : {money}, {user_id}, {username}")
        user = Users.query.filter_by(id=user_id).first()
        print(f"user :{user} , {type(user)} , {user.current_balance}")
        user.current_balance+= int(money)
        db.session.commit()

    if 'withdraw' in request.form:
        money = request.form["moneytowithdraw"]
        user_id = session["user_id"]
        username = session["user_name"]
        print(f"money : {money}, {user_id}, {username}")
        user = Users.query.filter_by(id=user_id).first()
        print(f"user :{user} , {type(user)} , {user.current_balance}")
        if user.current_balance >= int(money):
            user.current_balance -= int(money)
            db.session.commit()
        else:
            flash("Insufficient balance for withdrawal.", "error")

    return render_template("home/wallet.html",add_form=add_money, withdraw_form=withdraw_money)

@blueprint.route('/aitrade')
@login_required
def aitrade():
    return render_template("home/aitrade.html")

@blueprint.route('/create_trade', methods=['POST', 'GET'])
@login_required
def create_trade():
    form = TradeForm(request.form)

    if 'category' in request.form:
        category = request.form["category"]
        amount = request.form['tradelimit']
        duration = request.form['duration']
        uname = session['user_name']

        # print(f"category = {category}, amount = {amount}, duration = {duration}, uid = {uname}")
        make_trade(uname, amount, duration, stock_cap=category)
        
        return redirect( url_for('home_blueprint.dashboard'))
        
        
    return render_template("home/tradeform.html", form=form)


@blueprint.route('/dashboard')
@login_required
def dashboard():
    user_id = session["user_id"]
    username = session["user_name"]
    user = Users.query.filter_by(id=user_id).first()
    tran = Transaction.query.filter_by(uid=user.id).first()
    c=[]
    c.append(tran)
    print(c[0])
    return render_template("home/index.html",tran=c)





@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
