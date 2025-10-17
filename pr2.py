from functools import wraps


# 1) Декоратор логирования
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result

    return wrapper


# Примерные функции под логирование
@logger
def add(a, b):
    return a + b


@logger
def divide(a, b):
    if b == 0:
        return "Деление на ноль запрещено"
    return a / b


@logger
def greet(name):
    print(f"Привет, {name}!")
    # возвращает None


# 2) Декоратор доступа
def require_role(allowed_roles):
    """
    allowed_roles: список ролей (например, ["admin", "manager"])
    Ожидается, что первая позиция в аргументах — это user-словарь с ключами 'name' и 'role'.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            role = user.get("role")
            if role in allowed_roles:
                return func(user, *args, **kwargs)
            else:
                print(f"Доступ запрещён пользователю {user.get('name')}")
                return None

        return wrapper

    return decorator


# Пример использования декоратора доступа
@require_role(["admin"])
@logger
def delete_database(user):
    print(f"База данных удалена пользователем {user['name']}")
    return "OK"


@require_role(["admin", "manager"])
@logger
def view_stats(user):
    return f"Статистика доступна для {user['name']}"


# Тесты
if __name__ == "__main__":
    # ----- Тесты логгера -----
    add(2, 3)
    divide(10, 2)
    divide(5, 0)
    greet("Алексей")

    print("\n" + "-" * 50 + "\n")

    # ----- Тесты декоратора доступа -----
    admin = {"name": "Иван", "role": "admin"}
    manager = {"name": "Мария", "role": "manager"}
    guest = {"name": "Гость", "role": "guest"}

    # delete_database: только admin
    delete_database(admin)  # допустим
    delete_database(manager)  # запрещён
    delete_database(guest)  # запрещён

    print()

    # view_stats: admin и manager
    view_stats(admin)  # допустим
    view_stats(manager)  # допустим
    view_stats(guest)  # запрещён
