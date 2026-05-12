import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# הגדרת CORS - פעם אחת בלבד ובצורה נקייה
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# רשימת המניות שלך כולל אלו שציינת שקנית (TSEM, LXRX)
TICKERS = ["FNGU", "AVGO", "AMZN", "NFLX", "NVDA", "GOOGL", "META", "AAPL", "MU", "MSFT", "PLTR", "TSEM", "LXRX"]

async def get_ticker_data(client, ticker):
    # כאן צריכה להיות הלוגיקה של הקריאה ל-API (Alpha Vantage / Polygon)
    # לצורך הבדיקה, אני מחזיר נתון דמי כדי לוודא שהחיבור עובד
    return {
        "ticker": ticker, 
        "price": 100.0, 
        "open_price": 95.0, 
        "daily_change": 5.2
    }

@app.get("/")
async def root():
    return {"status": "online", "message": "Trading Backend is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async with httpx.AsyncClient() as client:
            while True:
                tasks = [get_ticker_data(client, ticker) for ticker in TICKERS]
                results = await asyncio.gather(*tasks)
                # סינון תוצאות ריקות
                valid_results = [r for r in results if r is not None]
                await websocket.send_json(valid_results)
                await asyncio.sleep(10) # עדכון כל 10 שניות
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
