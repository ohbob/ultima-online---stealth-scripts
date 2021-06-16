import uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import stealthScript

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/player")
def hello():
    stealthScript.updateobject()
    return stealthScript.player


@app.get("/journal")
def journal():
    stealthScript.updatejournal()
    return stealthScript.journal


@app.get("/log")
def log():
    return stealthScript.log


@app.get("/stats")
def stats():
    return stealthScript.stats


@app.get("/say")
def read_item(q: Optional[str] = None):
    return stealthScript.UOSay(q)


uvicorn.run(app, host="127.0.0.1", port=8000)
