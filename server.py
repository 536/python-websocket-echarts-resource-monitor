# !/usr/bin/env python3
# coding: utf-8
import asyncio
import json
import time

import psutil
import websockets

interval = 3  # update every 3s


async def analysis(websocket):
    while websocket.open:
        data = {
            "code": 0,
            "msg": "",
            "result": {
                "time": time.strftime('%M:%S'),
                "memory": psutil.virtual_memory().percent,
                "cpu": psutil.cpu_percent(),
                "disk": {
                    "C:": psutil.disk_usage('C:').percent,
                    "D:": psutil.disk_usage('D:').percent
                }
            }
        }
        print(data)
        await websocket.send(json.dumps(data))
        await asyncio.sleep(interval)

    print('closed')


async def main(host='localhost', port=5768):
    async with websockets.serve(analysis, host, port):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
