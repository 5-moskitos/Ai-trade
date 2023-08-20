import json
import random
from apps.authentication.models import Users
from apps.home.models import Transaction
from apps.home.models import Trade
from datetime import date
from apps import db
import numpy as np

def get_stock_data(stock_name):

    min_value = 100.0
    max_value = 200.0
    
    current_price = 150.0 

    
    past_30_days = [random.uniform(min_value, max_value) for _ in range(100)] # Replace with actual data

    
    future_10_days = [random.uniform(min_value, max_value) for _ in range(10)]

    # Create a dictionary with the collected data
    stock_data = {
        "stockname": stock_name,
        "data": {
            "current_price": current_price,
            "past_30_days": past_30_days,
            "future_10_days": future_10_days
        }
    }

    
    stock_data['pre_change_past'] = 100 * ((stock_data["data"]["current_price"] - stock_data["data"]["past_30_days"][-1])/stock_data["data"]["past_30_days"][-1])
    stock_data['pre_change_future'] = 100 * ((stock_data["data"]["future_10_days"][0] - stock_data["data"]["current_price"])/stock_data["data"]["future_10_days"][0])
    

    return json.dumps(stock_data, indent=4)


def get_all_stock_data(category):
    with open('apps/stocks.json', 'r') as fp:
        stock_names = json.load(fp)
    
    stock_names = stock_names[category]

        

    data = [json.loads(get_stock_data(stock)) for stock in stock_names]
    return data

def get_profit_data(stock_cap):
    invest = {}
    with open('apps/stocks.json', 'r') as fp:
        stock_names = json.load(fp)
    
    stock_names = stock_names[stock_cap][:10]

    invest['company'] = stock_names
    invest['probability'] = [random.uniform(0.01, 1) for _ in range(len(stock_names))] 
    invest["curr_price"] = [random.uniform(10, 1000) for _ in range(len(stock_names))]


    return invest

def make_trade(username, amount, duration, stock_cap="nifty50"):
    user = Users.query.filter_by(username=username).first()

    """ Calling Model server to get prediction for top 10 companies which will be most profitable in coming 10 days 
        update function name from get_profit_data to the one implemented in model side
    """
    amount = int(amount)
    duration = int(duration)

    invest = get_profit_data(stock_cap.lower())
    portions = [amount * factor for factor in invest['probability']]
    quantities = [cur_price/portion for cur_price, portion in zip(invest['curr_price'], portions)]
    i = 0

    transaction_id = []
    for company in invest['company']:
        transaction = Transaction(uid = user.id, date_time = date.today(), Stock_name = company, buySell = 1, Price=portions[i], quantity = quantities[i])
        db.session.add(transaction)
        db.session.flush()
        transaction_id.append(transaction.tran_id)
        i += 1

    print(transaction_id)
    tran_string = " ".join([str(x) for x in transaction_id])
    trade = Trade(user_id = user.id, tran_id = tran_string, category = stock_cap, duration = duration, amount = amount)
    
    db.session.add(trade)
    db.session.commit()







def reevaluation(app):
    app_context = app.app_context()
    app_context.push()

    ############# Code for calling finetuning function to fine tune model everyday ###########


    ############# Code for reevaluation of every trade in the trade table ####################

    trades = Trade.query.all()

    for trade in trades:
        user = Users.query.filter_by(id = trade.user_id).first()
        tran_ids = [int(x.strip()) for x in trade.tran_id.split(' ')]
        company_name = []
        buy_price = []
        quantity_bought = []
        trade_loss_threshold = 15
        company_loss_threshold = 10
        invested_amount = trade.amount

        
        for tran_id in tran_ids:
            tran = Transaction.query.filter_by(tran_id = tran_id).first()
            company_name.append(tran.Stock_name)
            buy_price.append(tran.Price)
            quantity_bought.append(tran.quantity)


        curr_price = []
        for company in company_name:
            data = json.loads(get_stock_data(company))
            curr_price.append(int(data["data"]["current_price"]))

        total_loss = 0

        for i in range(len(buy_price)):
            total_loss += ((buy_price[i]*quantity_bought[i]) - (curr_price[i]*quantity_bought[i]))
    
        tran_to_be_deleted = []
        new_inestment_amount = 0


        if total_loss >= ((trade_loss_threshold * invested_amount)/100):
            for tran_id in tran_ids:
                Transaction.query.filter_by(tran_id = tran_id).delete()
            Trade.query.filter_by(trade_id = trade.trade_id).delete()
            user.current_balance += sum(curr_price)
            """
                Display to user that his trade has been deleted as
                the loss exceeded beyond threshold
            """
        else:
            for i in range(len(company_name)):
                tran = Transaction.query.filter_by(tran_id = tran_ids[i]).first()
                company_amount_invested = tran.Price * tran.quantity
                if buy_price[i]*quantity_bought[i]-curr_price[i]*quantity_bought[i] >= ((company_loss_threshold * company_amount_invested)/100):
                    tran_to_be_deleted.append(tran.tran_id)
                    new_inestment_amount += curr_price[i]*quantity_bought[i]

            keep_transactions = []
            for tran_id in tran_ids:
                if tran_id not in tran_to_be_deleted:
                    keep_transactions.append(tran_id)

            invest = get_profit_data(trade.category.lower())

            company_new_invest = invest["company"]
            curr_price_new_invest = invest["curr_price"]
            probability = invest["probability"]
            
            sorted_combined_new_invest = sorted(list(zip(company_new_invest, curr_price_new_invest, probability)), key = lambda x: x[2])
            company_new_invest, curr_price_new_invest, probability = zip(* sorted_combined_new_invest)

            company_new_invest = company_new_invest[:len(tran_to_be_deleted)]
            curr_price_new_invest = curr_price_new_invest[:len(tran_to_be_deleted)]



            probability = probability[:len(tran_to_be_deleted)]
            exp_prob = np.exp(probability)
            exp_prob = exp_prob/sum(exp_prob)
            
            probability = exp_prob

            portions = [new_inestment_amount * factor for factor in probability]
            quantities = [cur_price/portion for cur_price, portion in zip(curr_price, portions)]

            for i in range(len(tran_to_be_deleted)):
                transaction = Transaction(uid = user.id, date_time = date.today(), Stock_name = company, buySell = 1, Price=portions[i], quantity = quantities[i])
                db.session.add(transaction)
                db.session.flush()
                keep_transactions.append(transaction.tran_id)

            
            tran_string = " ".join([str(x) for x in keep_transactions])
            trade.tran_id = tran_string
            
            for tran_id in tran_to_be_deleted:
                Transaction.query.filter_by(tran_id = tran_id).delete()

        db.session.commit()
        app_context.pop()