import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mock_db import USERS

app = FastAPI(title="Custom Auth System")
templates = Jinja2Templates(directory="templates")

@app.get("/register", response_class=HTMLResponse)
async def get_register_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.post("/auth/register", status_code=201)
async def register(    
    last_name: str = Form(...), first_name: str = Form(...), 
    email: str = Form(...), password: str = Form(...), password_repeat: str = Form(...)
):
    """Регистрация: создание юзера"""
    if password != password_repeat:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    
    new_user = {
        "id": len(USERS) + 1,
        "email": email,
        "role_id": 2, # Роль 'пользователь'
        "is_active": True,
        "first_name": first_name, "last_name": last_name
    }
    USERS.append(new_user)
    return {"status": "success", "message": "Успешная регистрация"}


@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    """Отображает страницу входа"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/auth/login")
async def login(data: UserLogin):
    """Логин: возвращает JWT токен"""
    user = next((u for u in USERS if u["email"] == data.email), None)
    if not user or not SecurityService.verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Неверные данные")
    
    if not user["is_active"]:
        raise HTTPException(status_code=401, detail="Аккаунт деактивирован")
    
    token = SecurityService.create_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)