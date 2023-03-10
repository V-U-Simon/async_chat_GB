""" 
1. Задание на закрепление знаний по модулю CSV. 
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, 
info_3.txt и формирующий новый «отчетный» файл в формате CSV. 
 
Для этого: 
 
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов 
с данными, их открытие и считывание данных. В этой функции из считанных данных 
необходимо с помощью регулярных выражений извлечь значения параметров 
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
Значения каждого параметра поместить в соответствующий список. Должно 
получиться четыре списка — например, os_prod_list, os_name_list, 
os_code_list, os_type_list. В этой же функции создать главный список 
для хранения данных отчета — например, main_data — и поместить в него 
названия столбцов отчета в виде списка: «Изготовитель системы», 
«Название ОС», «Код продукта», «Тип системы». Значения для этих 
столбцов также оформить в виде списка и поместить в файл main_data 
(также для каждого файла); 
 
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. 
В этой функции реализовать получение данных через вызов функции get_data(), 
а также сохранение подготовленных данных в соответствующий CSV-файл; 
 
Пример того, что должно получиться: 
 
Изготовитель системы,Название ОС,Код продукта,Тип системы 
 
1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based 
 
2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based 
 
3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based 
 
Обязательно проверьте, что у вас получается примерно то же самое. 
 
ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!! 
"""


from chardet.universaldetector import UniversalDetector
import re
from loguru_logger import logger
from pathlib import Path
import csv


@logger.catch
def main():
    folder = Path.cwd() / "lesson_02" / "data"
    data_files = folder.glob("info_*")
    headers = (
        "Название ОС",
        "Код продукта",
        "Тип системы",
        "Изготовитель системы",
    )
    logger.debug(f"📁 {folder.absolute()}")

    main_list = [get_data(file, headers=headers) for file in data_files]
    logger.debug(f"📦 common list: {logger.pretty(main_list)}")

    # create lists
    os_name_list = [item_list[headers.index("Название ОС")] for item_list in main_list]
    os_code_list = [item_list[headers.index("Код продукта")] for item_list in main_list]
    os_type_list = [item_list[headers.index("Тип системы")] for item_list in main_list]
    os_prod_list = [item_list[headers.index("Изготовитель системы")] for item_list in main_list]
    logger.info(f"📦 {os_prod_list}")
    logger.info(f"📦 {os_name_list}")
    logger.info(f"📦 {os_code_list}")
    logger.info(f"📦 {os_type_list}")
    write_to_csv(folder / "main_data", main_list)


def write_to_csv(file, data):
    with open(file, "w", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for i, row in enumerate(data, start=1):
            row.insert(0, i)
            logger.debug(f"{row}")
            writer.writerow(row)


def get_data(file, headers: list | tuple) -> list:
    logger.debug(f"📁 {file.absolute()}")

    propertry_data = {}
    encoding = get_file_ecnoding(file)

    with open(file, "r", encoding=encoding) as f:
        for line in f:
            for key in headers:
                if key in line:
                    propertry_data[key] = get_parsed_property(line)

    logger.debug(f"📦 {list(propertry_data.values())}")
    return list(propertry_data.values())


def get_parsed_property(line) -> str:
    pattern_separator = re.compile(r":")

    separator = re.search(pattern_separator, line)
    os_property = line[separator.end() :].strip()
    logger.info(f"🔍 parsed property: {os_property}")
    return os_property


def get_file_ecnoding(file) -> str:
    detector = UniversalDetector()

    with open(file, "br") as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()

    logger.debug(f"🔑 {detector.result['encoding']}")
    return detector.result["encoding"]


if __name__ == "__main__":
    main()
