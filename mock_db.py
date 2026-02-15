import bcrypt

# Функция-хелпер для генерации хеша
def get_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Имитация таблиц БД
ROLES = {1: "админ", 2: "пользователь"}
ELEMENTS = {"users": 1, "products": 2, "admin_panel": 3}

# Правила доступа: key = (role_id, element_id)
# Значение: набор прав
RULES = {
    (1, 1): {"read_all_permission": True, "update_all_permission": True}, # Админ к юзерам
    (1, 2): {"read_all_permission": True},                              # Админ к продуктам
    (1, 3): {"read_all_permission": True},                               # Админ к панели
    (2, 2): {"read_all_permission": True},                               # Юзер к продуктам
    # Для (2, 3) правила нет, значит доступ будет запрещен (403)
}

# Предзаполненный список пользователей (password: admin123)
USERS = [
    {
        "id": 1, 
        "email": "admin@example.com", 
        "password_hash": get_hash("admin123"), 
        "role_id": 1, 
        "is_active": True,
        "first_name": "Иван", "last_name": "Админов"
    }
]