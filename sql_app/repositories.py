
from sqlalchemy.orm import Session

from . import models, schemas


class DoctorRepo:
    
 async def create(db: Session, doctor: schemas.DoctorCreate):
        db_doctor = models.Doctor(ID_d=doctor.ID_d,Name= doctor.Name,Expertise= doctor.Expertise,Address= doctor.Address,Phone= doctor.Phone)
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    
 def fetch_by_id(db: Session,id):
     return db.query(models.Doctor).filter(models.Doctor.ID_d ==id).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Doctor).offset(skip).limit(limit).all()
 
 async def delete(db: Session,doctor_id):
     db_doctor= db.query(models.Doctor).filter_by(ID_d=doctor_id).first()
     db.delete(db_doctor)
     db.commit()
     
     
 async def update(db: Session,doctor_data):
    updated_doctor = db.merge(doctor_data)
    db.commit()
    return updated_doctor
    
    
    
class IllRepo:
    
    async def create(db: Session, ill: schemas.IllCreate):
        db_ill = models.Ill(ID=ill.ID,Name= ill.Name,Gender= ill.Gender,Age= ill.Age,Address= ill.Address,Phone= ill.Phone,User_name= ill.User_name,Password=ill.Password)
        db.add(db_ill)
        db.commit()
        db.refresh(db_ill)
        return db_ill
    
    def fetch_by_id(db: Session,id):
     return db.query(models.Ill).filter(models.Ill.ID == id).first()
 
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Ill).offset(skip).limit(limit).all()
 
    async def delete(db: Session,ill_id):
     db_ill= db.query(models.Ill).filter_by(ID=ill_id).first()
     db.delete(db_ill)
     db.commit()
     
     
    async def update(db: Session,ill_data):
     updated_ill = db.merge(ill_data)
     db.commit()
     return updated_ill


class TurnRepo:
    
    async def create(db: Session, turn: schemas.TurnCreate):
        db_turn = models.Turn(ID_n=turn.ID_n,Number= turn.Number,Date= turn.Date,Address= turn.Address,Cost= turn.Cost,ID_d= turn.ID_d,ID= turn.ID)
        db.add(db_turn)
        db.commit()
        db.refresh(db_turn)
        return db_turn
    
    def fetch_by_id(db: Session,id):
     return db.query(models.Turn).filter(models.Turn.ID_n == id).first()
 
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Turn).offset(skip).limit(limit).all()
 
    async def delete(db: Session,turn_id):
     db_turn= db.query(models.Turn).filter_by(ID_n=turn_id).first()
     db.delete(db_turn)
     db.commit()
     
     
    async def update(db: Session,turn_data):
     updated_turn = db.merge(turn_data)
     db.commit()
     return updated_turn


class Ill_DoctorRepo:
    
    async def create(db: Session, illdoctor: schemas.Ill_DoctorCreate):
        db_illdoctor = models.Ill_Doctor(ID_d= illdoctor.ID_d,ID= illdoctor.ID)
        db.add(db_illdoctor)
        db.commit()
        db.refresh(db_illdoctor)
        return db_illdoctor
    
    def fetch_by_id(db: Session,id):
     return db.query(models.Ill_Doctor).filter(models.Ill_Doctor.ID_d == id).first()
 
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Ill_Doctor).offset(skip).limit(limit).all()
 
    async def delete(db: Session,illdoctor_id):
     db_illdoctor= db.query(models.Ill_Doctor).filter_by(ID_d=illdoctor_id).first()
     db.delete(db_illdoctor)
     db.commit()
     
     
    async def update(db: Session,illdoctor_data):
     updated_illdoctor = db.merge(illdoctor_data)
     db.commit()
     return updated_illdoctor


class LoginRepo:
    
    async def create(db: Session, login: schemas.LoginCreate):
       db_login = models.Login(Username=login.Username,Password= login.Password,Phone= login.Phone)
       db.add(db_login)
       db.commit()
       db.refresh(db_login)
       return db_login
    
    def fetch_by_username(db: Session,username):
       return db.query(models.Login).filter(models.Login.Username ==username).first()

    def fetch_by_password(db: Session,password):
       return db.query(models.Login).filter(models.Login.Password ==password).first()
 
