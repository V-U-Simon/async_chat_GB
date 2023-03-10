""" 
3. Задание на закрепление знаний по модулю yaml. 
 Написать скрипт, автоматизирующий сохранение данных 
 в файле YAML-формата. 
Для этого: 
 
Подготовить данные для записи в виде словаря, в котором 
первому ключу соответствует список, второму — целое число, 
третьему — вложенный словарь, где значение каждого ключа — 
это целое число с юникод-символом, отсутствующим в кодировке 
ASCII(например, €); 
 
Реализовать сохранение данных в файл формата YAML — например, 
в файл file.yaml. При этом обеспечить стилизацию файла с помощью 
параметра default_flow_style, а также установить возможность работы 
с юникодом: allow_unicode = True; 
 
Реализовать считывание данных из созданного файла и проверить, 
совпадают ли они с исходными. 
"""


from loguru_logger import logger
import yaml
from pathlib import Path

file = Path.cwd() / "lesson_02" / "data" / "file.yaml"


data = {
    "items": ["computer", "printer", "keyboard", "mouse"],
    "items_quantity": 4,
    "items_ptice": {
        "computer": "200€-1000€",
        "printer": "100€-300€",
        "keyboard": "5€-50€",
        "mouse": "4€-7€",
    },
}


with open(file, "w", encoding="utf-8") as f:
    yaml.dump(
        data,
        f,
        default_flow_style=False,
        sort_keys=True,
    )


with open(file, "r", encoding="utf-8") as f:
    # data = yaml.load(f, Loader=yaml.Loader)
    data = yaml.safe_load(f)
    logger.debug(logger.pretty(data))
