from datetime import datetime
import requests

file = 'dec_logs.txt'

def get_log(path):
    def decor(func):
        def foo(*args, **kwargs):
            date = datetime.now()
            name = func.__name__
            result = func(*args, **kwargs)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(f'Дата и время: {date}\n'
                f'Имя функции: {name}\n'
                f'Аргументы: {args, kwargs}\n'
                f'Результат: {result}\n')
            return result
        return foo
    return decor

@get_log(file)
def get_status(*args, **kwargs):
    url1 = ','.join(args)
    response = requests.get(url=url1)
    return response.status_code