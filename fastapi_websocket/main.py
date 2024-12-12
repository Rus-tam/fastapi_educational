from fastapi import FastAPI
import asyncio
import websockets
import json

app = FastAPI()


async def fetch_bybit_candles(symbol: str, interval: str):
    """Подключение к Bybit WebSocket API и вывод данных в консоль"""
    url = "wss://stream.bybit.com/v5/public/linear"
    subscription_params = {"op": "subscribe", "args": [f"kline.{interval}.{symbol}"]}

    try:
        async with websockets.connect(url) as ws:
            await ws.send(json.dumps(subscription_params))
            print(f"Subscribed to kline data for {symbol} {interval}")

            while True:
                response = await ws.recv()
                data = json.loads(response)

                print(" ")
                print(data)
                print(" ")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection to Bybit WebSocket closed: {e}")
    except Exception as e:
        print(f"Error in Bybit WebSocket: {e}")


@app.get("/candles")
async def get_candles(symbol: str = "BTCUSDT", interval: str = "1m"):
    print(f"Starting to fetch candle data for {symbol} with interval {interval}")
    asyncio.create_task(fetch_bybit_candles(symbol, interval))
    return {"status": "Fetching data in the background. Check logs for output."}
