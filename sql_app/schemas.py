from typing import List, Optional

from pydantic import BaseModel


class DoctorBase(BaseModel):

    ID_d : int
    Name : str
    Expertise : str
    Address : str
    Phone : int


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    pass

    class Config:
        orm_mode = True


class IllBase(BaseModel):

    ID : int
    Name : str
    Gender : str  
    Age : int
    Address : str
    Phone : int
    User_name : str


class IllCreate(IllBase):
    Password : str
    pass


class Ill(IllBase):
    pass

    class Config:
        orm_mode = True


class TurnBase(BaseModel):

    ID_n : int
    Number : int
    Date : str
    Address : str
    Cost : int
    ID_d : int
    ID : int


class TurnCreate(TurnBase):
    pass


class Turn(TurnBase):
    pass

    class Config:
        orm_mode = True


class Ill_DoctorBase(BaseModel):

    ID_d : int
    ID : int


class Ill_DoctorCreate(Ill_DoctorBase):
    pass


class Ill_Doctor(Ill_DoctorBase):
    pass

    class Config:
        orm_mode = True

class LoginBase(BaseModel):

    Username : str
    Password : str
    Phone : int


class LoginCreate(LoginBase):
    pass


class Login(LoginBase):
    pass

    class Config:
        orm_mode = True