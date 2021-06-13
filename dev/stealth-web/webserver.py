# pip install websockets
# pip install fastapi

import codecs
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import onmessage

app = FastAPI()
html = codecs.open("index.html", 'r').read()

# html = html.replace("Date.now()", '"Random Nickname"')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/obj")
async def get():
    return onmessage.obj


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if await onmessage.onMessage(data):

                # add messages to the log
                for message in onmessage.broadcast:
                    await manager.broadcast(f"{message}")
                    onmessage.broadcast.pop(0)

                await manager.send_personal_message(f"Executed: {data}", websocket)
            else:
                await manager.broadcast(f"Client #{client_id} There is no such command: {data}")


    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000)