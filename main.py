import uvicorn
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
        "id": 1,
        "email": email,
        "role_id": 2, # Роль 'пользователь'
        "is_active": True,
        "first_name": first_name, "last_name": last_name
    }
    return {"status": "success", "message": "Успешная регистрация"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)