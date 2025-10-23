from fastapi import APIRouter, Depends, Form # <-- Assurez-vous d'importer Form
from fastapi.templating import Jinja2Templates
from database import get_session
from models import Produit, User, ProduitForm, UserForm
from .admin_factory import create_admin_crud_router

# Initialise le routeur principal de l'admin
router = APIRouter(prefix="/admin")


templates = Jinja2Templates(directory="templates")


# --- DÉPENDANCE DE FORMULAIRE POUR PRODUIT ---
# Cette fonction lit le formulaire et retourne un modèle ProduitForm
def get_produit_form(
    type_p: str = Form(...),
    designation_p: str = Form(...),
    prix_ht: float = Form(...),
    stock_p: int = Form(...)
) -> ProduitForm:
    return ProduitForm(
        type_p=type_p,
        designation_p=designation_p,
        prix_ht=prix_ht,
        stock_p=stock_p
    )

# --- DÉPENDANCE DE FORMULAIRE POUR USER ---
def get_user_form(
    user_login: str = Form(...),
    user_mail: str = Form(...),
    user_password: str = Form(...),
    user_compte_id: int = Form(...)
) -> UserForm:
    return UserForm(
        user_login=user_login,
        user_mail=user_mail,
        user_password=user_password,
        user_compte_id=user_compte_id
    )


# Crée les routes CRUD pour les Produits
produits_router = create_admin_crud_router(
    model=Produit,
    form_dependency=Depends(get_produit_form), 
    session_dep=Depends(get_session),
    templates=templates,
    parent_prefix= router.prefix ,
    prefix="/produits",
    list_template="admin_produits.html",
    form_template="admin_produit_form.html",
    pk_name="id_p"
)

# Crée les routes CRUD pour les Utilisateurs
users_router = create_admin_crud_router(
    model=User,
    form_dependency=Depends(get_user_form), 
    session_dep=Depends(get_session),
    templates=templates,
    parent_prefix= router.prefix ,
    prefix="/users",
    list_template="admin_users.html",
    form_template="admin_user_form.html",
    pk_name="user_id"
)

# Inclut les routeurs générés dans le routeur admin principal
router.include_router(produits_router)
router.include_router(users_router)