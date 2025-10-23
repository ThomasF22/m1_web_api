from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel

class User(SQLModel, table=True):
    __tablename__ = "user"
    user_id: int | None = Field(default=None, primary_key=True)
    user_login: str
    user_password: str
    user_mail: str
    user_compte_id : int # ajouter pour correspondre a la db dans la roadmap
    user_date_new: datetime
    user_date_login: datetime | None = None


class Produit(SQLModel, table=True):
    __tablename__ = "produit"
    id_p: int   | None = Field(default=None, primary_key=True)
    type_p: str
    designation_p: str
    #description_p: str | None = None
    prix_ht: float
    date_in: datetime
    timeS_in: datetime
    stock_p: int

class ProduitForm(BaseModel):
    """Modèle Pydantic pour le formulaire Produit"""
    type_p: str
    designation_p: str
    #description_p : str
    prix_ht: float
    stock_p: int

class UserForm(BaseModel):
    """Modèle Pydantic pour le formulaire User"""
    user_login: str
    user_mail: str
    user_password: str
    user_compte_id: int