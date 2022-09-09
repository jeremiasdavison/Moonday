from flask import Flask, render_template
from main import actualCrypto, dayReportETH, dayReportBTC, dayReportSOL, dayReportADA
import json, requests, claves
import main

app = Flask(__name__)
@app.route('/')
def Index():
    aeth, abtc, aada, asol = actualCrypto()
    eth_low, eth_high = dayReportETH()
    btc_low, btc_high = dayReportBTC()
    sol_low, sol_high = dayReportSOL()
    ada_low, ada_high = dayReportADA()

    consulta = json.loads(requests.get(f"https://min-api.cryptocompare.com/data/v2/news/?lang=ES{claves.clave}").text)
    
    url = consulta['Data'][0]['url']
    url2 = consulta['Data'][1]['url']
    url3 = consulta['Data'][2]['url']
    url4 = consulta['Data'][3]['url']

    msg = (consulta['Data'][0]['title'])
    msg2 = (consulta['Data'][1]['title'])
    msg3 = (consulta['Data'][2]['title'])
    msg4 = (consulta['Data'][3]['title'])


    return render_template('index.html', aeth = aeth, abtc = abtc, aada = aada, asol = asol, 
    eth_low = eth_low, eth_high = eth_high, 
    btc_low = btc_low, btc_high = btc_high, 
    sol_low = sol_low, sol_high = sol_high,
    ada_low = ada_low, ada_high = ada_high, 
    url = url, url2 = url2, url3 = url3, 
    url4 = url4, msg = msg, msg2 = msg2, 
    msg3 = msg3, msg4 = msg4)

if __name__ == '__main__':    
    app.run(debug=True, port=4000)