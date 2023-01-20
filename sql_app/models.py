from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base


class Doctor(Base):
    __tablename__ = "doctor"
    
    ID_d = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Expertise = Column(String, nullable=False)
    Address = Column(String, nullable=False)
    Phone = Column(Integer, nullable=False,unique=True)

    def __repr__(self):
        return 'DoctorModel(Name=%s, Expertise=%s,Phone=%s)' % (self.Name, self.Expertise,self.Phone)

class Ill(Base):
    __tablename__ = "ill"

    ID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    User_name = Column(String, nullable=False,unique=True)
    Password = Column(String, nullable=False)
    Gender = Column(String, nullable=False)    
    Age = Column(Integer, nullable=False)
    Address = Column(String, nullable=False)
    Phone = Column(Integer, nullable=False,unique=True)

    def __repr__(self):
        return 'Ill(Name=%s, Gender=%s,Age=%s,Phone=%s)' % (self.Name, self.Gender,self.Age,self.Phone)

class Turn(Base):
    __tablename__ = "turn"
    
    ID_n = Column(Integer, primary_key=True)
    Number = Column(Integer, nullable=False)
    Date = Column(String, nullable=False)
    Address = Column(String, nullable=False)
    Cost = Column(Integer, nullable=False)
    ID_d = Column(Integer,ForeignKey('doctor.ID_d'),nullable=False)
    ID = Column(Integer,ForeignKey('ill.ID'),nullable=False)

    def __repr__(self):
        return 'TurnModel(Number=%s, Date=%s,Address=%s)' % (self.Number, self.Date,self.Address)

class Ill_Doctor(Base):
    __tablename__ = "ill_doctor"

    ID_d = Column(Integer,primary_key=True)
    ID = Column(Integer,ForeignKey('ill.ID'),nullable=False)

    def __repr__(self):
        return 'Ill_DoctorModel(ID=%s, ID_d=%s)' % (self.ID, self.ID_d)

class Login(Base):
    __tablename__ = "login"
    
    Username = Column(String, primary_key=True)
    Password = Column(String, nullable=False)
    Phone = Column(Integer,unique=True, nullable=False)

    def __repr__(self):
        return 'LoginModel(Username=%s, Phone=%s)' % (self.Username, self.Phone)