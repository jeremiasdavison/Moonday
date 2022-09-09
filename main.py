import requests
import json
import time
import datetime
import schedule
from pyowm import OWM
import claves
from telegram.ext import *
import os

status = True
def dayReportETH():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=USD&limit=1{claves.clave}").text)
    return consulta['Data']['Data'][1]['low'], consulta['Data']['Data'][1]['high']
eth_low, eth_high = dayReportETH()

def dayReportBTC():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=1{claves.clave}").text)
    return consulta['Data']['Data'][1]['low'], consulta['Data']['Data'][1]['high']
btc_low, btc_high = dayReportBTC()

def dayReportSOL():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=SOL&tsym=USD&limit=1{claves.clave}").text)
    return consulta['Data']['Data'][1]['low'], consulta['Data']['Data'][1]['high']
sol_low, sol_high = dayReportSOL()

def dayReportADA():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=ADA&tsym=USD&limit=1{claves.clave}").text)
    return consulta['Data']['Data'][1]['low'], consulta['Data']['Data'][1]['high']
ada_low, ada_high = dayReportADA()

def actualCrypto():
    consultaBTC = json.loads(requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD{claves.clave}').text)["USD"]
    consultaETH = json.loads(requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD{claves.clave}').text)["USD"]
    consultaSOL = json.loads(requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=SOL&tsyms=USD{claves.clave}').text)["USD"]
    consultaADA = json.loads(requests.get(f'https://min-api.cryptocompare.com/data/price?fsym=ADA&tsyms=USD{claves.clave}').text)["USD"]

    return int(consultaETH), int(consultaBTC), consultaADA, consultaSOL

def sendMsg(mensaje):
    send_text = f'{claves.telegram}{mensaje}'
    response = requests.get(send_text)
    return response.json()

def weather():
    owm = OWM(claves.owm)
    mgr = owm.weather_manager()
    clima = mgr.weather_at_place('Buenos Aires, Argentina')
    w = clima.weather
    return f'Temperature is {w.temperature("celsius")["temp"]}°⛅'

def top_list():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/top/totalvolfull?limit=10&tsym=USD{claves.clave}").text)
    top = ''
    for x in range(10):
        msg = (consulta['Data'][x]['CoinInfo']["FullName"])
        top = top + msg +'\n'
    return f'Top List ⏫: \n{top}'

def news_report():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/v2/news/?lang=ES{claves.clave}").text)
    new = ''
    for x in range(5):
        msg = (consulta['Data'][x]['title'])
        url = consulta['Data'][x]['url']
        new = new + msg + "\n" + url +'\n'
    return f'Day News {datetime.date.today()}📰: \n{new}'

def sentiment():
    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest?fsym=BTC{claves.clave}").text)
    sentiment_msg = (consulta['Data']["inOutVar"]["sentiment"])
    return f'Today the market is: {sentiment_msg}'

        
def dailyReport():
    global eth_low, eth_high, btc_low, btc_high
    eth_low, eth_high = dayReportETH()
    btc_low, btc_high = dayReportBTC()
    sol_low, sol_high = dayReportSOL()
    ada_low, ada_high = dayReportADA()
    return f'Daily Report of {datetime.date.today()}📅\n\n{sentiment()}\nBTC 📈: {btc_high} 📉: {btc_low}\nETH 📈: {eth_high} 📉: {eth_low}\nADA 📈: {ada_high} 📉: {ada_low}\nSOL  📈: {sol_high} 📉: {sol_low}'

def socket():
    pass

def minutesReport():
    global eth_high, eth_low, btc_high, btc_low, ada_low, ada_high, sol_low, sol_high
    actualETH, actualBTC, actualADA, actualSOL = actualCrypto()

    if actualBTC < btc_low:    
        sendMsg(f'BTC LOW:      {actualBTC}')
        btc_low = actualBTC - 100   # Esto lo hacemos para que avise cuando baje un precio relativo
    elif actualBTC > btc_high:
        sendMsg(f'BTC HIGH:     {actualBTC}')
        btc_high = actualBTC + 100 
        
    if actualETH < eth_low:
        sendMsg(f'ETH LOW:      {actualETH}')
        eth_low = actualETH - 50
    elif actualETH > eth_high:
        sendMsg(f'ETH HIGH:     {actualETH}')
        eth_high = actualETH + 50 

    if actualADA  < ada_low:
        sendMsg(f'ADA LOW:      {actualADA}')
        ada_low = actualADA - 0.01
    elif actualADA > ada_high:
        sendMsg(f'ADA HIGH:     {actualADA}')
        ada_high = actualADA + 0.01

    if actualSOL < sol_low:
        sendMsg(f'SOL LOW:      {actualSOL}')
        sol_low = actualSOL - 5
    elif actualSOL > sol_high:
        sendMsg(f'SOL HIGH:     {actualSOL}')
        sol_high = actualSOL + 5      

def handle_message(update, ctx):
    text = str(update.message.text)
    update.message.reply_text(text)

def command_alive(update, ctx):
    update.message.reply_text('I´m Alive👓')
def command_price(update, ctx):
    update.message.reply_text(dailyReport())
def command_toplist(update, ctx):
    update.message.reply_text(top_list())
def command_news(update, ctx):
    update.message.reply_text(news_report())
def command_actual(update, ctx):
    actualETH, actualBTC, actualADA, actualSOL = actualCrypto()
    update.message.reply_text(f'BTC: {actualBTC}\nETH: {actualETH}\nSOL: {actualSOL}\nADA: {actualADA}')
def command_status(update, ctx):
    global status
    if status == False:
        status = True
        update.message.reply_text('The Bot is On')
    else:
        status = False
        update.message.reply_text('The Bot is Off')

#############################################

if __name__ == '__main__':    
    if status == True:
        try:
            schedule.every().day.at("00:30").do(sendMsg(dailyReport()))
            schedule.every().day.at("11:00").do(sendMsg(dailyReport()))
            schedule.every().day.at("11:00").do(sendMsg(news_report()))
            schedule.every(1).minutes.do(minutesReport())
        except:
            pass
    
    try:
        updater = Updater(claves.telegram_key, use_context=True)
        dp = updater.dispatcher
        #Commands handlers
        dp.add_handler(CommandHandler('toplist', command_toplist))
        dp.add_handler(CommandHandler('price', command_price))
        dp.add_handler(CommandHandler('alive', command_alive))
        dp.add_handler(CommandHandler('news', command_news))
        dp.add_handler(CommandHandler('status', command_status))
        dp.add_handler(CommandHandler('actual', command_actual))

        updater.start_polling(1.0)
    except:
        sendMsg('No se pudo ejecutar el comando') 
                    
"""              
                            ---     Ideas   ---
        .   Mandar por un socket informacion de Urgencias para usuarios
"""