from slowapi import Limiter
from slowapi.util import get_remote_address

# Инициализируем лимитер, чтобы импортировать его в роутеры и main.py
limiter = Limiter(key_func=get_remote_address)