from flask import Flask, render_template
import yfinance as yf
import datetime

app = Flask(__name__)

data_sinyal = [] # buat nyimpen riwayat

@app.route("/")
def home():
    global data_sinyal
    try:
        data = yf.download("XAUUSD=X", period="1d", interval="1m")
        harga = float(data['Close'].iloc[-1])
        harga_sebelum = float(data['Close'].iloc[-2])
        
        if harga > harga_sebelum:
            sinyal = "BUY"
        else:
            sinyal = "SELL"
            
        tp = harga + 2000
        sl = harga - 2000
        waktu = datetime.datetime.now().strftime("%H:%M:%S")
        
        data_sinyal.append({"waktu": waktu, "harga": round(harga, 2), "hasil": sinyal})
        if len(data_sinyal) > 5:
            data_sinyal.pop(0)
        
    except:
        harga, sinyal, tp, sl, waktu = 0, "WAIT", 0, 0, "--:--"
    
    return render_template("index.html", harga=round(harga,2), sinyal=sinyal, tp=round(tp,2), sl=round(sl,2), waktu=waktu, data_sinyal=data_sinyal)

if __name__ == "__main__":
    app.run()
