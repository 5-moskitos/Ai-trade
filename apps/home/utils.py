import json
import random

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
    with open('/media/aftab/Work/Ai-trade/apps/stocks.json', 'r') as fp:
        stock_names = json.load(fp)
    
    stock_names = stock_names[category]

        

    data = [json.loads(get_stock_data(stock)) for stock in stock_names]
    print(data)
    return data

