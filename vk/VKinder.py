import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_functions import search_users, get_photo, sort_likes, json_create
from vk.models import engine, Session, write_message, reg_user, add_user, add_user_photos, check_db_user, check_db_black, check_db_favorites, check_db_master, add_to_blacklist, delete_db_blacklist, delete_db_favorites
from vk_config import token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
session = Session()
connection = engine.connect()

def loop_bot():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id

def menu_bot(id_num):
    write_message(id_num,
    f'Вас приветствует бот - VKinder\n'
    f'\nЗарегистрируйтесь если вы используете его первый раз\n'
    f'Для регистрации введите - /reg\n'
    f'Если вы уже зарегистрированы - начинайте поиск\n'
    f'\nДля поиска\n'
    f'Перейти в избранное нажмите - 2\n'
    f'Перейти в черный список - 0\n')

def show_info():
    write_message(user_id, f'Это была последняя анкета'
    f'Перейти в избранное - 2'
    f'Перейти в черный список - 0'
    f'Поиск'
    f'Меню бота')

def reg_new_user(id_num):
    write_message(id_num, 'Вы прошли регистрацию')
    write_message(id_num, f'"VKinder" - для активации бота\n')
    reg_user(id_num)

def go_to_favorites(ids):
    alls_users = check_db_favorites(ids)
    write_message(ids, f'Избранные анкеты:')
    for nums, users in enumerate(alls_users):
        write_message(ids, f'{users.name}, {users.surname}, {users.link}')
        write_message(ids, '1 - Удалить из избранного, 2 - Далее\n q - Выход')
        message_text, user_ids = loop_bot()
        if message_text == '2':
            if nums >= len(alls_users) - 1:
                write_message(user_ids, f'Это была последняя анкета\n'
                f'"VKinder" - вернуться в меню\n')
        elif message_text == '1':
            delete_db_favorites(users.vk_id)
            write_message(user_ids, f'Анкета успешно удалена')
            if nums >= len(alls_users) - 1:
                write_message(user_ids, f'Это была последняя анкета\n'
                f'"VKinder" - вернуться в меню\n')
        elif message_text.lower() == 'q':
            write_message(ids, '"VKinder" - для активации бота')
            break

def go_to_blacklist(ids):
    all_users = check_db_black(ids)
    write_message(ids, f'Анкеты в черном списке:')
    for num, user in enumerate(all_users):
        write_message(ids, f'{user.first_name}, {user.second_name}, {user.link}')
        write_message(ids, '1 - Удалить из черного списка, 2 - Далее\n q - Выход')
        message_text, user_ids = loop_bot()
        if message_text == '2':
            if num >= len(all_users) - 1:
                write_message(user_ids, f'Это была последняя анкета\n'
                f'"VKinder" - вернуться в меню\n')
        elif message_text == '1':
            print(user.id)
            delete_db_blacklist(user.vk_id)
            write_message(user_ids, f'Анкета удалена')
            if num >= len(all_users) - 1:
                write_message(user_ids, f'Это была последняя анкета\n'
                f'"VKinder" - вернуться в меню\n')
        elif message_text.lower() == 'q':
            write_message(ids, '"VKinder" - для активации бота')
            break

if __name__ == '__main__':
    while True:
        message_text, user_id = loop_bot()
        if message_text == "VKinder":
            menu_bot(user_id)
            message_text, user_id = loop_bot()
            if message_text.lower() == '/reg':
                reg_new_user(user_id)
            elif len(message_text) > 1:
                gender = 0
                if message_text[0:7].lower() == 'Девушка':
                    gender = 1
                elif message_text[0:7].lower() == 'Мужчина':
                    gender = 2
                age_at = message_text[8:10]
                if int(age_at) < 18:
                    write_message(user_id, 'Минимальный возраст - 18 лет')
                    age_at = 18
                age_to = message_text[11:14]
                if int(age_to) >= 100:
                    write_message(user_id, 'Максимальный возраст - 99 лет')
                    age_to = 99
                city = message_text[14:len(message_text)].lower()
                result = search_users(gender, int(age_at), int(age_to), city)
                json_create(result)
                current_user_id = check_db_master(user_id)

                for i in range(len(result)):
                    dating_user, blocked_user = check_db_user(result[i][3])
                    user_photo = get_photo(result[i][3])
                    if user_photo == 'Нет фото' or dating_user is not None or blocked_user is not None:
                        continue
                    sorted_user_photo = sort_likes(user_photo)
                    write_message(user_id, f'\n{result[i][0]}  {result[i][1]}  {result[i][2]}', )
                    try:
                        write_message(user_id, f'Фото:',
                        attachment=','.join
                      ([sorted_user_photo[-1][1], sorted_user_photo[-2][1],
                        sorted_user_photo[-3][1]]))
                    except IndexError:
                        for photo in range(len(sorted_user_photo)):
                            write_message(user_id, f'Фото:',
                            attachment=sorted_user_photo[photo][1])
                    write_message(user_id, '1 - Добавить, 2 - Далее, \n q - Выход из поиска')
                    message_text, user_id = loop_bot()
                    if message_text == '2':
                        if i >= len(result) - 2:
                            show_info()
                    elif message_text == '1':
                        if i >= len(result) - 1:
                            show_info()
                            break
                        try:
                            add_user(user_id, result[i][3], result[i][1],
                            result[i][0], city, result[i][2], current_user_id.id)
                            add_user_photos(user_id, sorted_user_photo[0][1],
                            sorted_user_photo[0][0], current_user_id.id)
                        except AttributeError:
                            write_message(user_id, 'Вы не зарегистрировались\n'
                            'Введите "VKinder", чтобы перезагрузить бота')
                            break
                    elif message_text == '2':
                        if i >= len(result) - 1:
                            show_info()
                        add_to_blacklist(user_id, result[i][3], result[i][1],
                        result[i][0], city, result[i][2],
                        sorted_user_photo[0][1],
                        sorted_user_photo[0][0], current_user_id.id)
                    elif message_text.lower() == 'q':
                        write_message(user_id, 'Введите "VKinder" для активации бота')
                        break
            elif message_text == '2':
                go_to_favorites(user_id)
            elif message_text == '0':
                go_to_blacklist(user_id)