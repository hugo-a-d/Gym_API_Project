import re
from datetime import date as Date, datetime
from typing import Annotated, Optional
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, BeforeValidator, ConfigDict
from db import get_conn, init_db
from utils import ScaleWeight, RowerCardio


app = FastAPI()

    
@app.on_event("startup") # look up Lifespan events as this old
def startup():
    init_db()

@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")


@app.post("/rower", status_code=201)
def add_cardio(entry: RowerCardio):
    with get_conn() as con:
        cur = con.execute(
            """INSERT INTO RowerCardio
               (date, duration_min, distance_m, avg_500m)
               VALUES (?, ?, ?, ?)""",
            (entry.date.isoformat(), entry.duration_min,
             entry.distance_m, entry.avg_500m,),
        )
    return {"id": cur.lastrowid}

@app.post("/weight", status_code=201)
def add_weight(entry: ScaleWeight):
    with get_conn() as con:
        cur = con.execute(
            """INSERT INTO ScaleWeight (date, weight_kg, body_fat, muscle_mass)
               VALUES (?, ?, ?, ?)""",
            (entry.date.isoformat(), entry.weight_kg, entry.body_fat,
             entry.muscle_mass),
        )
    return {"id": cur.lastrowid}