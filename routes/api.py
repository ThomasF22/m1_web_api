from datetime import datetime
from fastapi import APIRouter, Form, Depends, HTTPException
from sqlmodel import Session, select
from models import User
from database import get_session

router = APIRouter(prefix="/api")

# Endpoints API Backend

@router.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/users/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users")
def create_user(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.user_mail==email)).first():
        raise HTTPException(status_code=400, detail="Email already in use")
    user = User(user_login=email, user_mail=email, user_password=password, user_date_new=datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created", "user_id": user.user_id}

@router.put("/users/{user_id}")
def update_user(user_id: int, email: str | None = Form(None), password: str | None = Form(None), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if email:
        user.user_login = email
        user.user_mail = email
    if password:
        user.user_password = password
    session.add(user)
    session.commit()
    return {"message": "User updated", "user_id": user.user_id}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": f"User {user_id} deleted"}
