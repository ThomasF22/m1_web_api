from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select, SQLModel, func
from pydantic import BaseModel
from typing import Type
from datetime import datetime
from fastapi.templating import Jinja2Templates
from models import  Produit, User

# --- permet de trouver le produit en utlisant sa pk
def get_item_or_404(session: Session, model: Type[SQLModel], pk_name: str, item_id: int):
    """
    Remplace session.get() en utilisant select().where()
    """
    # Récupère la colonne de la clé primaire (ex: Produit.id_p)
    pk_column = getattr(model, pk_name) 
    
    item = session.exec(select(model).where(pk_column == item_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    return item


def create_admin_crud_router(
    model: Type[SQLModel],
    form_dependency: BaseModel,        
    session_dep: Session,
    templates: Jinja2Templates,
    parent_prefix: str,
    prefix: str,
    list_template: str,
    form_template: str,
    pk_name: str
):
    """
    Génère un APIRouter complet pour le CRUD admin d'un modèle.
    """
    router = APIRouter(prefix=prefix)
    redirect_url = parent_prefix + prefix
    
    
    #  LISTER (GET /)
    @router.get("/", response_class=HTMLResponse)
    def admin_list(request: Request, session: Session = session_dep):
        items = session.exec(select(model)).all()
        return templates.TemplateResponse(
            list_template, 
            {"request": request, "context_items": items}
        )

    #  AFFICHER FORMULAIRE (Nouveau) (GET /new)
    @router.get("/new", response_class=HTMLResponse)
    def admin_form_new(request: Request):
        return templates.TemplateResponse(
            form_template, 
            {"request": request, "context_item": None}
        )
    
    #  TRAITER FORMULAIRE (Nouveau) (POST /new)
    @router.post("/new", response_class=RedirectResponse)
    def admin_create(session: Session = session_dep, form_data: BaseModel = form_dependency):
        
        data_dict = form_data.model_dump()
        
        if model == Produit:
            data_dict['date_in'] = datetime.now()
            data_dict['timeS_in'] = datetime.now()
        if model == User:

            max_id = session.scalar(select(func.max(User.user_compte_id)))
            new_compte_id = (max_id or 0) + 1
            data_dict['user_compte_id'] = new_compte_id

            data_dict['user_date_new'] = datetime.now()
            data_dict['user_date_login'] = datetime.now()
            
        db_item = model(**data_dict)
        
        session.add(db_item)
        session.commit()
        return RedirectResponse(url=redirect_url, status_code=303)

    #  AFFICHER FORMULAIRE (Modifier) (GET /edit/{item_id})
    @router.get("/edit/{item_id}", response_class=HTMLResponse)
    def admin_form_edit(request: Request, item_id: int, session: Session = session_dep):
        # On remplace session.get() par notre helper
        db_item = get_item_or_404(session, model, pk_name, item_id)
        
        return templates.TemplateResponse(
            form_template, 
            {"request": request, "context_item": db_item}
        )

    #  TRAITER FORMULAIRE (Modifier) (POST /edit/{id})
    @router.post("/edit/{item_id}", response_class=RedirectResponse)
    def admin_update(item_id: int, session: Session = session_dep, form_data: BaseModel = form_dependency):
        
        db_item = get_item_or_404(session, model, pk_name, item_id)
            
        form_data_dict = form_data.model_dump(exclude_unset=True)
        for key, value in form_data_dict.items():
            setattr(db_item, key, value)
            
        session.add(db_item)
        session.commit()
        return RedirectResponse(url=redirect_url, status_code=303)


    #  SUPPRIMER (POST /delete/{id})
    @router.post("/delete/{item_id}", response_class=RedirectResponse)
    def admin_delete(item_id: int, session: Session = session_dep):
        
        # On remplace session.get() par notre helper
        db_item = get_item_or_404(session, model, pk_name, item_id)
            
        session.delete(db_item)
        session.commit()
        return RedirectResponse(url=redirect_url, status_code=303)

    return router