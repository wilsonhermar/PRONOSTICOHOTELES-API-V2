from pydantic import BaseModel
from typing import Dict, List

class HotelIn(BaseModel):
    nombre:str

class HotelOut(BaseModel):
    nombre:str
    ubicacion:str
    estrellas:str
    totalHabitaciones:int
    sencilla:int
    precioMinSenc:int
    doble:int
    precioMinDob:int
    triple:int
    precioMinTrip:int
    suite:int
    precioMinSuite:int
    Tasa:List[Dict[str, float]]

class TempOut(BaseModel):
    Tasa:List[Dict[str, float]]

class CostOut(BaseModel):
    precioMinSenc:int
    precioMinDob:int
    precioMinTrip:int
    precioMinSuite:int
    Tasa:List[Dict[str, float]]

