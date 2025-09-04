from fastapi import FastAPI 
from analysis.technical import get_technical_signal 
from analysis.ml_model import predict_signal 
 
app = FastAPI() 
 
@app.get("/signal") 
def get_signal(symbol: str, timeframe: str = "1h"): 
    tech = get_technical_signal(symbol, timeframe) 
    ml = predict_signal(symbol, timeframe) 
    return { 
        "symbol": symbol, 
        "timeframe": timeframe, 
        "technical": tech, 
        "ml": ml 
    }



from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SmartSignalBot is running!"}
