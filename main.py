from db.hotel_db import HotelInDB
from db.hotel_db import get_hotel, create_hotel, delete_hotel, update_hotel
from models.hotel_models import HotelIn, HotelOut, TempOut,CostOut


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


@app.get("/temp/search/{nombre},{mes}")
async def get_temp(nombre: str, mes:int):
    ref_in_db = get_hotel(nombre)
    if ref_in_db == None:
        raise HTTPException(status_code=404, detail="EL REGISTRO NO EXISTE EN LA BASE DE DATOS")
    ocup = TempOut(**ref_in_db.dict()) 
    mes=mes-1
    o=ocup.Tasa[mes]
    meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    coef=o.get(meses[mes])
    if coef<=0.5:Temp='Baja'
    elif coef>0.5 and coef<=0.75:Temp='Media'
    elif coef>0.75 and coef<=1.0:Temp='Alta'
    mensaje="En el mes de "+meses[mes]+" la temporada es "+Temp
    return mensaje

@app.get("/costo/search/{nombre},{mes},{tipo}")
async def get_cost(nombre: str, mes:int, tipo:str):
    ref_in_db = get_hotel(nombre)
    if ref_in_db == None:
        raise HTTPException(status_code=404, detail="EL REGISTRO NO EXISTE EN LA BASE DE DATOS")
    ocup = CostOut(**ref_in_db.dict()) 
    mes=mes-1
    o=ocup.Tasa[mes]
    meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    coef=o.get(meses[mes])
    if coef<=0.5:Temp='Baja'
    elif coef>0.5 and coef<=0.75:Temp='Media'
    elif coef>0.75 and coef<=1.0:Temp='Alta'
    if tipo=='sencilla':precioprom=ocup.precioMinSenc
    elif tipo=='doble':precioprom=ocup.precioMinDob
    elif tipo=='triple':precioprom=ocup.precioMinTrip
    elif tipo=='suite':precioprom=ocup.precioMinSuite
    if Temp=='Baja':Costo=precioprom-(precioprom*(coef/2))
    elif Temp=='Media':Costo=precioprom+(precioprom*(coef/3))
    elif Temp=='Alta':Costo=precioprom+(precioprom*(coef/2))  
    return (tipo,Costo)

