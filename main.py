import uvicorn
import jwt
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas import UserLogin
from security import SecurityService, PermissionChecker
from mock_db import USERS

app = FastAPI(title="Custom Auth System")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("401.html", {"request": request}, status_code=401)


@app.exception_handler(403)
async def forbidden_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("403.html", {"request": request}, status_code=403)


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


# Mock-View для демонстрации прав доступа
@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    """Доступ к товарам только если в RULES прописано read_all_permission
    Отдает только визуальную оболочку страницы"""
    return templates.TemplateResponse("products.html", {"request": request})


@app.get("/api/products")
async def get_products_data(user: dict = Depends(PermissionChecker("products", "read_all"))):
    """
    Реальный API, который требует токен. 
    Сюда запрос придет от JavaScript с заголовком Authorization.
    """
    return {"items": ["Ноутбук", "Смартфон", "Наушники"], "user": user["email"]}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)