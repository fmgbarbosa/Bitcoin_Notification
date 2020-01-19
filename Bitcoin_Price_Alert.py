
#Get bitcoin prices - coin market cap API
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas
#import requests
import datetime
import time

#Input values
bot_chatID = '@<Insert chat_id>'

def get_coin_data():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    
    parameters = {
        'id':'1,1027,52', #Identificar as crypto a extrair
        'convert':'EUR' #Selecionar a fiat para apresentar o valor
    }

    #Enviar a Key da API de forma mais segura
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '<Insert API key>',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data


def format_message(data):
    #Create array of dictionaries 
    list_coin =[]
    for coin_id in data['data']:
        coin = {}
        coin['id'] = coin_id
        coin['name'] = data['data'][coin_id]['name']
        coin['price_eur'] = round(data['data'][coin_id]['quote']['EUR']['price'],2)
        coin['update_date'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M') #save current datetime
        list_coin.append(coin)
    
    message = 'Crypto Alert! ' +"\n" + "\n"\
    + list_coin[0]['name'] + 'Price Eur: ' + str(list_coin[0]['price_eur']) + "\n"\
    + list_coin[1]['name'] + 'Price Eur: ' + str(list_coin[1]['price_eur']) + "\n"\
    + list_coin[2]['name'] + 'Price Eur: ' + str(list_coin[2]['price_eur'])
    
    return message


def send_message(bot_chatID,bot_message):
    bot_token = '<Insert bot token>'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    print(bot_message)
    response = requests.get(send_text)

    return response.json

def main():
    
    while True:
        data = get_coin_data()
        message = format_message(data)
        send_message(bot_chatID,message)

        time.sleep(1 * 60) #sleep for 1min

#Só executa a função main se o script for executado pelo terminal
if __name__ == '__main__':
    main()
