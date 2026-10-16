from datetime import date as Date
from typing import Optional
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from db import get_conn, init_db


app = FastAPI()

class rower_cardio(BaseModel):
    date : Date
    distance_m : Optional[float] = None
    avg_500m : Optional[float] = None


class scale_weight(BaseModel):
    date : Date
    weight_kg : Optional[float] = None
    body_fat : Optional[float] = None
    muscle_mass: Optional[float] = None
    
@app.on_event("startup") # look up Lifespan events as this old
def startup():
    init_db()

@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")


@app.post("/cardio")
def add_cardio(entry: rower_cardio):
    with get_conn() as con:
        cur = con.execute(
            """INSERT INTO cardio
               (date, activity, duration_min, distance_km, avg_hr, max_hr, calories, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (entry.date.isoformat(), entry.activity, entry.duration_min,
             entry.distance_km, entry.avg_hr, entry.max_hr,
             entry.calories, entry.notes),
        )
    return {"id": cur.lastrowid}

@app.post("/weight", status_code=201)
def add_weight(entry: scale_weight):
    with get_conn() as con:
        cur = con.execute(
            """INSERT INTO weight (date, weight_kg, body_fat, muscle_mass_kg,
                                   water_pct, bmi, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (entry.date.isoformat(), entry.weight_kg, entry.body_fat,
             entry.muscle_mass),
        )
    return {"id": cur.lastrowid}