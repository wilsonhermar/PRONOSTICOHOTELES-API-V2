from pydantic import BaseModel

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


