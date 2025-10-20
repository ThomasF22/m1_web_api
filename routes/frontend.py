from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from datetime import datetime
from database import get_session
from models import User
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# Endpoints API Frontend

@router.get("/", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_user(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.user_mail==email, User.user_password==password)).first()
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email ou mot de passe invalide"})
    user.user_date_login = datetime.now()
    session.add(user)
    session.commit()
    return templates.TemplateResponse("welcome.html", {"request": request, "user_login": user.user_login, "user_date_login": user.user_date_login.strftime("%d/%m/%Y %H:%M:%S")})

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def register_user(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.user_mail==email)).first()
    if existing:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email déjà utilisée"})
    user = User(user_login=email, user_mail=email, user_password=password, user_date_new=datetime.now())
    session.add(user)
    session.commit()
    return RedirectResponse("/login", status_code=303)


@router.get("/produits", response_class=HTMLResponse)
def produits_list(request: Request, session: Session = Depends(get_session)):
    from models import Produit
    produits = session.exec(select(Produit)).all()
    # produits is a list of Produit objects; pass to template
    return templates.TemplateResponse("produits.html", {"request": request, "produits": produits})
