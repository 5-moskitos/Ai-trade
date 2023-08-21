import json
import random
from apps.authentication.models import Users
from apps.home.models import Transaction
from apps.home.models import Trade
from datetime import date
from apps import db
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
    invest['probability'] = [random.uniform(0, 1) for _ in range(len(stock_names))] 
    invest["curr_price"] = [random.uniform(10, 1000) for _ in range(len(stock_names))]


    return invest

def make_trade(username, amount, duration, stock_cap="nifty50"):
    user = Users.query.filter_by(username=username).first()

    """ Calling Model server to get prediction for top 10 companies which will be most profitable in coming 10 days 
        update function name from get_profit_data to the one implemented in model side
    """
    user_amount = user.current_balance
    amount = int(amount)
    duration = int(duration)
    if amount > user_amount:
        print('insufficient balance in wallet')
        return 
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







def reevaluation():
    pass