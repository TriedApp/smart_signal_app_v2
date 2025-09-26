from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/signal')
def signal():
    # خروجی تستی برای اتصال اپلیکیشن
    return jsonify({
        "symbol": "BTC",
        "signal": "buy",
        "entry_price": 27100,
        "exit_price": 27800,
        "confidence": 0.87
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)