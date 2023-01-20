from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import time
import asyncio
from starlette.responses import RedirectResponse


import sql_app.models as models
import sql_app.schemas as schemas
from db import get_db, engine
from sql_app.repositories import DoctorRepo, IllRepo , TurnRepo , Ill_DoctorRepo , LoginRepo

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get('/login/{login_u}', tags=["Login"], response_model=schemas.Login)
def get_login(login_u : str, db: Session = Depends(get_db)):
    """
    Get the User with the given Username provided by User stored in database
    """
    db_login = LoginRepo.fetch_by_username(db, login_u)
    if db_login is None:
        raise HTTPException(status_code=404, detail="User not found with the given Username")
    return db_login


@app.post('/login', tags=["Login"], response_model=schemas.Login, status_code=201)
async def create_login(login_request: schemas.LoginCreate, db: Session = Depends(get_db)):
    """
    Create a User and store it in the database
    """

    db_login = LoginRepo.fetch_by_username(db, username=login_request.Username)
    if db_login:
        raise HTTPException(status_code=400, detail="User already exists!")

    return await LoginRepo.create(db=db, login=login_request)



@app.post('/doctor', tags=["Doctor"], response_model=schemas.Doctor, status_code=201)
async def create_doctor(doctor_request: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a Doctor and store it in the database
    """

    db_doctor = DoctorRepo.fetch_by_id(db, id=doctor_request.ID_d)
    if db_doctor:
        raise HTTPException(status_code=400, detail="Doctor already exists!")

    return await DoctorRepo.create(db=db, doctor=doctor_request)


@app.get('/doctor', tags=["Doctor"], response_model=List[schemas.Doctor])
def get_all_Doctor(db: Session = Depends(get_db)):
    """
    Get all the Doctors stored in database
    """
    return DoctorRepo.fetch_all(db)


@app.get('/doctor/{doctor_id}', tags=["Doctor"], response_model=schemas.Doctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get the Doctor with the given ID provided by User stored in database
    """
    db_doctor = DoctorRepo.fetch_by_id(db, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found with the given ID")
    return db_doctor


@app.delete('/doctor/{doctor_id}', tags=["Doctor"])
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Delete the Doctor with the given ID provided by User stored in database
    """
    db_doctor = DoctorRepo.fetch_by_id(db, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found with the given ID")
    await DoctorRepo.delete(db, doctor_id)
    return "Doctor deleted successfully!"


@app.put('/doctor/{doctor_id}', tags=["Doctor"], response_model=schemas.Doctor)
async def update_doctor(doctor_id: int, doctor_request: schemas.Doctor, db: Session = Depends(get_db)):
    """
    Update an Doctor stored in the database
    """
    db_doctor = DoctorRepo.fetch_by_id(db, doctor_id)
    if db_doctor:
        update_doctor_encoded = jsonable_encoder(doctor_request)
        db_doctor.ID_d = update_doctor_encoded['ID_d']
        db_doctor.Name = update_doctor_encoded['Name']
        db_doctor.Expertise = update_doctor_encoded['Expertise']
        db_doctor.Address = update_doctor_encoded['Address']
        db_doctor.Phone = update_doctor_encoded['Phone']
        return await DoctorRepo.update(db=db, doctor_data=db_doctor)
    else:
        raise HTTPException(status_code=400, detail="Doctor not found with the given ID")


@app.post('/ill', tags=["Ill"], response_model=schemas.Ill, status_code=201)
async def create_ill(ill_request: schemas.IllCreate, db: Session = Depends(get_db)):
    """
    Create an Ill and store it in the database
    """

    db_ill = IllRepo.fetch_by_id(db, id=ill_request.ID)
    if db_ill:
        raise HTTPException(status_code=400, detail="Ill already exists!")

    return await IllRepo.create(db=db, ill=ill_request)


@app.get('/ill', tags=["Ill"], response_model=List[schemas.Ill])
def get_all_Ill(db: Session = Depends(get_db)):
    """
    Get all the Ills stored in database
    """
    return IllRepo.fetch_all(db)


@app.get('/ill/{ill_id}', tags=["Ill"], response_model=schemas.Ill)
def get_ill(ill_id: int, db: Session = Depends(get_db)):
    """
    Get the Ill with the given ID provided by User stored in database
    """
    db_ill = IllRepo.fetch_by_id(db, ill_id)
    if db_ill is None:
        raise HTTPException(status_code=404, detail="Ill not found with the given ID")
    return db_ill


@app.delete('/ill/{ill_id}', tags=["Ill"])
async def delete_ill(ill_id: int, db: Session = Depends(get_db)):
    """
    Delete the Ill with the given ID provided by User stored in database
    """
    db_ill = IllRepo.fetch_by_id(db, ill_id)
    if db_ill is None:
        raise HTTPException(status_code=404, detail="Ill not found with the given ID")
    await IllRepo.delete(db, ill_id)
    return "Ill deleted successfully!"


@app.put('/ill/{ill_id}', tags=["Ill"], response_model=schemas.Ill)
async def update_ill(ill_id: int, ill_request: schemas.IllBase, db: Session = Depends(get_db)):
    """
    Update an Ill stored in the database
    """
    db_ill = IllRepo.fetch_by_id(db, ill_id)
    if db_ill:
        update_ill_encoded = jsonable_encoder(ill_request)
        db_ill.ID = update_ill_encoded['ID']
        db_ill.Name = update_ill_encoded['Name']
        db_ill.Gender = update_ill_encoded['Gender']
        db_ill.Age = update_ill_encoded['Age']
        db_ill.Address = update_ill_encoded['Address']
        db_ill.Phone = update_ill_encoded['Phone']
        db_ill.User_name = update_ill_encoded['User_name']
        return await IllRepo.update(db=db, ill_data=db_ill)
    else:
        raise HTTPException(status_code=400, detail="Ill not found with the given ID")


@app.post('/turn', tags=["Turn"], response_model=schemas.Turn, status_code=201)
async def create_turn(turn_request: schemas.TurnCreate, db: Session = Depends(get_db)):
    """
    Create an Turn and store it in the database
    """

    db_turn = TurnRepo.fetch_by_id(db, id=turn_request.ID_n)
    if db_turn:
        raise HTTPException(status_code=400, detail="Turn already exists!")

    return await TurnRepo.create(db=db, turn=turn_request)


@app.get('/turn', tags=["Turn"], response_model=List[schemas.Turn])
def get_all_Turn(db: Session = Depends(get_db)):
    """
    Get all the Turns stored in database
    """
    return TurnRepo.fetch_all(db)


@app.get('/turn/{turn_id}', tags=["Turn"], response_model=schemas.Turn)
def get_turn(turn_id: int, db: Session = Depends(get_db)):
    """
    Get the Turn with the given ID provided by User stored in database
    """
    db_turn = TurnRepo.fetch_by_id(db, turn_id)
    if db_turn is None:
        raise HTTPException(status_code=404, detail="Turn not found with the given ID")
    return db_turn


@app.delete('/turn/{turn_id}', tags=["Turn"])
async def delete_turn(turn_id: int, db: Session = Depends(get_db)):
    """
    Delete the Turn with the given ID provided by User stored in database
    """
    db_turn = TurnRepo.fetch_by_id(db, turn_id)
    if db_turn is None:
        raise HTTPException(status_code=404, detail="Turn not found with the given ID")
    await TurnRepo.delete(db, turn_id)
    return "Turn deleted successfully!"


@app.put('/turn/{turn_id}', tags=["Turn"], response_model=schemas.Turn)
async def update_turn(turn_id: int, turn_request: schemas.Turn, db: Session = Depends(get_db)):
    """
    Update an Turn stored in the database
    """
    db_turn = TurnRepo.fetch_by_id(db, turn_id)
    if db_turn:
        update_turn_encoded = jsonable_encoder(turn_request)
        db_turn.ID_n = update_turn_encoded['ID_n']
        db_turn.Number = update_turn_encoded['Number']
        db_turn.Date = update_turn_encoded['Date']
        db_turn.Address = update_turn_encoded['Address']
        db_turn.Cost = update_turn_encoded['Cost']
        db_turn.ID_d = update_turn_encoded['ID_d']
        db_turn.ID = update_turn_encoded['ID']
        return await TurnRepo.update(db=db, turn_data=db_turn)
    else:
        raise HTTPException(status_code=400, detail="Turn not found with the given ID")


@app.post('/illdoctor', tags=["IllDoctor"], response_model=schemas.Ill_Doctor, status_code=201)
async def create_illdoctor(illdoctor_request: schemas.Ill_DoctorCreate, db: Session = Depends(get_db)):
    """
    Create an IllDoctor and store it in the database
    """

    db_illdoctor = Ill_DoctorRepo.fetch_by_id(db, id=illdoctor_request.ID_d)
    if db_illdoctor:
        raise HTTPException(status_code=400, detail="IllDoctor already exists!")

    return await Ill_DoctorRepo.create(db=db, illdoctor=illdoctor_request)


@app.get('/illdoctor', tags=["IllDoctor"], response_model=List[schemas.Ill_Doctor])
def get_all_IllDoctor(db: Session = Depends(get_db)):
    """
    Get all the IllDoctor stored in database
    """
    return Ill_DoctorRepo.fetch_all(db)


@app.get('/illdoctor/{illdoctor_id}', tags=["IllDoctor"], response_model=schemas.Ill_Doctor)
def get_illdoctor(illdoctor_id: int, db: Session = Depends(get_db)):
    """
    Get the IllDoctor with the given ID provided by User stored in database
    """
    db_illdoctor = Ill_DoctorRepo.fetch_by_id(db, illdoctor_id)
    if db_illdoctor is None:
        raise HTTPException(status_code=404, detail="IllDoctor not found with the given ID")
    return db_illdoctor


@app.delete('/illdoctor/{illdoctor_id}', tags=["IllDoctor"])
async def delete_illdoctor(illdoctor_id: int, db: Session = Depends(get_db)):
    """
    Delete the IllDoctor with the given ID provided by User stored in database
    """
    db_illdoctor = Ill_DoctorRepo.fetch_by_id(db, illdoctor_id)
    if db_illdoctor is None:
        raise HTTPException(status_code=404, detail="IllDoctor not found with the given ID")
    await Ill_DoctorRepo.delete(db, illdoctor_id)
    return "IllDoctor deleted successfully!"


@app.put('/illdoctor/{illdoctor_id}', tags=["IllDoctor"], response_model=schemas.Ill_Doctor)
async def update_illdoctor(illdoctor_id: int, illdoctor_request: schemas.Ill_DoctorBase, db: Session = Depends(get_db)):
    """
    Update an IllDoctor stored in the database
    """
    db_illdoctor = Ill_DoctorRepo.fetch_by_id(db, illdoctor_id)
    if db_illdoctor:
        update_illdoctor_encoded = jsonable_encoder(illdoctor_request)
        db_illdoctor.ID_d = update_illdoctor_encoded['ID_d']
        db_illdoctor.ID = update_illdoctor_encoded['ID']
        
        return await Ill_DoctorRepo.update(db=db, illdoctor_data=db_illdoctor)
    else:
        raise HTTPException(status_code=400, detail="IllDoctor not found with the given ID")

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
