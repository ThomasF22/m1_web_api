from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "user"
    user_id: int | None = Field(default=None, primary_key=True)
    user_login: str
    user_password: str
    user_mail: str
    user_date_new: datetime
    user_date_login: datetime | None = None
