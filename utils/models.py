import re
from datetime import date as Date, datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, ConfigDict

def parse_split(value):
    if value is None or value == "":
        return None
    if isinstance(value, str):
        m = re.fullmatch(r"(\d{1,2}):([0-5]\d(?:\.\d+)?)", value.strip())
        if not m:
            raise ValueError("Use m:ss, for example 2:05 or 2:05.3")
        return int(m.group(1)) * 60 + float(m.group(2))
    return value   # plain numbers (seconds) still work

Split = Annotated[Optional[float], BeforeValidator(parse_split)]

class RowerCardio(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    date : Date
    duration_min : Optional[float] = None
    distance_m : Optional[float] = None
    avg_500m : Split = None


class ScaleWeight(BaseModel):
    date : Date
    weight_kg : Optional[float] = None
    body_fat : Optional[float] = None
    muscle_mass: Optional[float] = None