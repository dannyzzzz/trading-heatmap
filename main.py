import asyncio
import httpx
import pandas as pd
import ta
from datetime import datetime, timezone
import time
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

API_KEY = "d7vouj1r01qj3ct7skmgd7vouj1r01qj3ct7skn0"
TICKERS = ["FNGU", "AVGO", "AMZN", "NFLX", "NVDA", "GOOGL", "META", "AAPL", "MU", "MSFT", "PLTR"]

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


async def get_ticker_data(client, ticker):
    try:
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"
        resp = await client.get(quote_url)
        q = resp.json()

        if 'c' not in q or q['c'] == 0: return None

        curr = q['c']
        open_p = q.get('o', curr)

        # d = Change, dp = Percent Change (מאתמול)
        daily_pct = q.get('dp', 0)

        return {
            "ticker": ticker,
            "price": float(curr),
            "open_price": float(open_p),
            "daily_change": float(daily_pct),
            "updated": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        print(f"Error {ticker}: {e}")
        return None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with httpx.AsyncClient() as client:
        while True:
            try:
                tasks = [get_ticker_data(client, t) for t in TICKERS]
                res = await asyncio.gather(*tasks)
                valid = [r for r in res if r is not None]
                await websocket.send_json(valid)
                await asyncio.sleep(20)
            except:
                break


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)