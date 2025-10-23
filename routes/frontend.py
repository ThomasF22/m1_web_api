from fastapi import APIRouter, Form, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select, func
from datetime import datetime
from database import get_session
from models import User, Produit
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
    return RedirectResponse(url="/admin", status_code=303)

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def register_user(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.user_mail==email)).first()
    if existing:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email déjà utilisée"})
    #ajout user_compte_id
    max_id = session.scalar(select(func.max(User.user_compte_id)))
    new_compte_id = (max_id or 0) + 1

    user = User(user_login=email, 
                user_mail=email, 
                user_password=password, 
                user_compte_id=new_compte_id, 
                user_date_new=datetime.now(), 
                user_date_login=datetime.now()
                )
    session.add(user)
    session.commit()
    return RedirectResponse("/login", status_code=303)


@router.get("/produits", response_class=HTMLResponse)
def produits_list(request: Request, session: Session = Depends(get_session)):
    produits = session.exec(select(Produit)).all()
    # produits is a list of Produit objects; pass to template
    return templates.TemplateResponse("produits.html", {"request": request, "produits": produits})

"""
@router.get("/admin/produits", response_class=HTMLResponse)
def admin_produits_list(request: Request, session: Session = Depends(get_session)):
    #Affiche la page admin avec la liste des produits.
    produits = session.exec(select(Produit)).all()
    return templates.TemplateResponse(
        "admin_produits.html", 
        {"request": request, "produits": produits}
    )
"""



"""
# AFFICHER LE FORMULAIRE (pour "Nouveau")
@router.get("/admin/produits/new", response_class=HTMLResponse)
def admin_produit_form_new(request: Request):
    #Affiche le formulaire de création de produit (vide).
    return templates.TemplateResponse(
        "admin_produit_form.html", 
        {"request": request, "produit": None} # On envoie 'None'
    )

# TRAITER LE FORMULAIRE (pour "Nouveau")
@router.post("/admin/produits/new", response_class=RedirectResponse)
def admin_produit_create(
    session: Session = Depends(get_session),
    type_p: str = Form(...),
    designation_p: str = Form(...),
    #description_p: str | None = Form(None),
    prix_ht: float = Form(...),
    stock_p: int = Form(...)
):
    #Crée le nouveau produit en BDD (logique copiée de api.py)
    prod = Produit(
        type_p=type_p, 
        designation_p=designation_p, 
        #description_p=description_p, 
        prix_ht=prix_ht, 
        date_in=datetime.now(), 
        timeS_in=datetime.now(), 
        stock_p=stock_p
    )
    session.add(prod)
    session.commit()
    
    # Redirige vers la liste admin
    return RedirectResponse(url="/admin/produits", status_code=303)


# AFFICHER LE FORMULAIRE (pour "Modifier")
@router.get("/admin/produits/edit/{id_p}", response_class=HTMLResponse)
def admin_produit_form_edit(request: Request, id_p: int, session: Session = Depends(get_session)):
    #Affiche le formulaire pré-rempli pour modifier un produit.
    prod = session.get(Produit, id_p)
    if not prod:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
        
    return templates.TemplateResponse(
        "admin_produit_form.html", 
        {"request": request, "produit": prod} # On envoie le produit
    )

# TRAITER LE FORMULAIRE (pour "Modifier")
@router.post("/admin/produits/edit/{id_p}", response_class=RedirectResponse)
def admin_produit_update(
    id_p: int,
    session: Session = Depends(get_session),
    type_p: str = Form(...),
    designation_p: str = Form(...),
    #description_p: str | None = Form(None),
    prix_ht: float = Form(...),
    stock_p: int = Form(...)
):
    #Met à jour le produit en BDD (logique copiée de api.py)
    prod = session.get(Produit, id_p)
    if not prod:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
        
    # Mise à jour des champs
    prod.type_p = type_p
    prod.designation_p = designation_p
    #prod.description_p = description_p
    prod.prix_ht = prix_ht
    prod.stock_p = stock_p
    
    session.add(prod)
    session.commit()
    
    return RedirectResponse(url="/admin/produits", status_code=303)


#TRAITER LA SUPPRESSION (DELETE)
@router.post("/admin/produits/delete/{id_p}", response_class=RedirectResponse)
def admin_produit_delete(id_p: int, session: Session = Depends(get_session)):
    #Supprime le produit (logique copiée de api.py)
    prod = session.get(Produit, id_p)
    if not prod:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
        
    session.delete(prod)
    session.commit()
    
    return RedirectResponse(url="/admin/produits", status_code=303)
"""