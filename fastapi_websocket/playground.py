import asyncio
import websockets
import json


async def bybit_candles():
    url = "wss://stream.bybit.com/v5/public/spot"

    # Параметры подписки на свечи. Замените 'BTCUSDT' и '1m' на нужные вам.
    subscription_params = {"op": "subscribe", "args": ["kline.1.BTCUSDT"]}

    async with websockets.connect(url) as websocket:
        # Подписка на свечи
        await websocket.send(json.dumps(subscription_params))
        print("Subscribed to kline data")

        while True:
            try:
                # Получение данных
                response = await websocket.recv()
                data = json.loads(response)

                print(" ")
                print(data)
                print(" ")

            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed: {e}")
                break


if __name__ == "__main__":
    asyncio.run(bybit_candles())
