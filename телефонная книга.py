from pprint import pprint
import re 
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

phone = re.compile(r'(\+7|8)?\s*\((\d+)\)\s*(\d+)[\s-]*(\d+)[\s-]*(\d+)')
text = re.compile(r'(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё]\w+[А-яЁё –]*\–*\s*)*\,*(\+*\d\s*\(*\d+\)*\-*\s*\d+\-*\d+\-*\d+\s*\(*\w*\.*\s*\d*\)*)*\,*(\w+\.*\w*\@\w+\.\w+)*')

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
new_contacts_list = []
for i in range(len(contacts_list)):
    if i == 0:
        new_contacts_list.append(contacts_list[i])
    else:
        line = ','.join(contacts_list[i])
        result = re.search(text, line)
        new_contacts_list.append(list(result.groups()))
        if new_contacts_list[i][0] in new_contacts_list:
            print(new_contacts_list[i][0:3])
        if new_contacts_list[i][5] != 0:
            new_contacts_list[i][5] = phone.sub(r'+7(\2)\3-\4-\5', new_contacts_list[i][5])

final_contacts_list = []
for i in range(len(new_contacts_list)):
    for j in range(len(new_contacts_list)):
        if new_contacts_list[i][0] == new_contacts_list[j][0]:
            new_contacts_list[i] = [x or y for x, y in zip(new_contacts_list[i], new_contacts_list[j])]
    if new_contacts_list[i] not in final_contacts_list:
        final_contacts_list.append(new_contacts_list[i])
        
pprint(final_contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)

input()