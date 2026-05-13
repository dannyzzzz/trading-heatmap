import asyncio
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# הגדרת CORS חזקה במיוחד
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TICKERS = ["FNGU", "AVGO", "AMZN", "NFLX", "NVDA", "GOOGL", "META", "AAPL", "MU", "MSFT", "PLTR"]

@app.get("/")
async def root():
    return {"status": "online", "info": "Connect to /ws for data"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # נתוני בדיקה כדי לוודא שהמפה נפתחת
            data = [{"ticker": t, "price": 100.0, "daily_change": 1.5} for t in TICKERS]
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    # שימוש בפורט ש-Render נותן לנו, או 10000 כברירת מחדל
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
