from datetime import datetime
import requests

def get_log(func):
    def foo(*args, **kwargs):
        date = datetime.now()
        name = func.__name__
        result = func(*args, **kwargs)
        with open('decoratorlogs.txt', 'w', encoding='utf-8') as file:
            file.write(f'Дата и время: {date}\n'
            f'Имя: {name}\n'
            f'Аргументы: {args, kwargs}\n'
            f'Результат: {result}\n')
        return result
    return foo

@get_log
def get_status(*args, **kwargs):
    url1 = ','.join(args)
    response = requests.get(url=url1)
    return response.status_code