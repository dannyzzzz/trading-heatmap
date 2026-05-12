import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# זה החלק שפותר את "שגיאת חיבור" - הוא פותח את האבטחה
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # מאפשר לכל האתרים להתחבר
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TICKERS = ["FNGU", "AVGO", "AMZN", "NFLX", "NVDA", "GOOGL", "META", "AAPL", "MU", "MSFT", "PLTR", "TSEM", "LXRX"]

# דף נחיתה כדי שלא תראה "Not Found"
@app.get("/")
async def root():
    return {"message": "The server is UP and running!", "websocket_path": "/ws"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # נתונים זמניים לבדיקה
            data = [{"ticker": t, "price": 150.0, "daily_change": 2.5} for t in TICKERS]
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
