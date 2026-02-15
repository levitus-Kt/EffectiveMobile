import jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from mock_db import USERS, RULES, ELEMENTS

SECRET_KEY = "gghu9u5toihfhg84nuhdfy94y98thh"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class SecurityService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        # bcrypt требует bytes
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def create_token(user_id: int) -> str:
        return jwt.encode({"sub": str(user_id)}, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Идентифицирует пользователя по JWT токену (имитация запроса к БД)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Неверный токен")
    
    # Ищем пользователя в нашем списке
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user or not user["is_active"]:
        raise HTTPException(status_code=401, detail="Пользователь не найден или удален")
    return user

class PermissionChecker:
    """Проверяет права доступа роли к конкретному элементу"""
    def __init__(self, element: str, action: str):
        self.element = element
        self.action = action

    def __call__(self, user: dict = Depends(get_current_user)):
        elem_id = ELEMENTS.get(self.element)
        rule = RULES.get((user["role_id"], elem_id), {})
        if not rule.get(f"{self.action}_permission", False):
            raise HTTPException(status_code=403, detail="Доступ запрещен (недостаточно прав)")
        return user