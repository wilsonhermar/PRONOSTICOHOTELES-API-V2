from db.hotel_db import HotelInDB
from db.hotel_db import get_hotel, create_hotel, delete_hotel, update_hotel
from models.hotel_models import HotelIn, HotelOut

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", "http://localhost:8000", "http://localhost:8082",
]

app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/test/")
async def check_conexion():
    return {"LA APLICACION ESTA CONECTADA"}

@app.post("/hotel/verification/")
async def check_hotel(check: HotelIn):
    hotel_in_db = get_hotel(check.nombre)
    if hotel_in_db == None:
        raise HTTPException(status_code=404, detail="EL REGISTRO NO EXISTE EN LA BASE DE DATOS")
    return {"EL REGISTRO EXISTE EN LA BASE DE DATOS"}

@app.get("/hotel/search/{nombre}")
async def get_Hotel(name: str):
    hotel_in_db = get_hotel(name)
    if hotel_in_db == None:
        raise HTTPException(status_code=404, detail="EL REGISTRO NO EXISTE EN LA BASE DE DATOS")
    hotel_out = HotelOut(**hotel_in_db.dict())
    return hotel_out

@app.post("/hotel/create")
async def create_new_hotel(newHotel: HotelOut):
    hotel_in_db = get_hotel(newHotel.nombre)
    if hotel_in_db == None:
        create_hotel(newHotel)
        return {"EL REGISTRO SE CREO EN LA BASE DE DATOS"}
    else:
        raise HTTPException(status_code=404, detail="EL REGISTRO NO SE PUEDE CREAR YA EXISTE EN LA BASE DE DATOS")

@app.delete("/hotel/delete/{nombre}")
async def delete_this_hotel(nombre: str):
    hotel_in_db = get_hotel(nombre)
    if hotel_in_db ==None:
        raise HTTPException(status_code=404, detail="EL REGISTRO NO SE PUEDE BORRAR NO EXISTE EN LA BASE DE DATOS")
    delete_hotel(nombre)
    return{"EL REGISTRO SE BORRRO DE LA BASE DE DATOS"}

@app.put("/hotel/update/")
async def update_this_hotel(updateHotel: HotelOut):
    hotel_in_db = get_hotel(updateHotel.nombre)
    if hotel_in_db == None:
         raise HTTPException(status_code=404, detail="EL REGISTRO NO EXISTE EN LA BASE DE DATOS NO SE PUEDE ACTUALIZAR")
    update_hotel(updateHotel)
    return {"EL REGISTRO SE ACTUALIZO DE MANERA CORRECTA"}