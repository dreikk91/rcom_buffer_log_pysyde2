import logging
from datetime import datetime

import colorama
from pymongo import MongoClient

logging.basicConfig(filename="clear_rcom_buffer.log", level=logging.DEBUG)
logging.info("Starting program")
client = MongoClient("mongodb://localhost:27017/")
db = client.DBClientsPPK
listy = []
dt_string = datetime.now()
colorama.init()

msg_list = {
    104: "нет сети 220в ",
    105: "Восстановление сети 220В ",
    63: "Проверка связи:  УСПЕШНО ",
    106: "Питание для аккумулятора в норме ",
    64: "Взят под охрану ",
    8: "Идентификация ответственного ",
    107: "Аккумулятор разряжен ",
    120: "Шлейф неисправен ",
    88: "Норма шлейфа  ",
    48: "Открыта крышка",
    58: 'Авария питания (1) Модуль "СМ16" ',
    108: "Открыта дверца ",
    109: "Закрыта дверца ",
    72: "Снят с охраны ",
    80: "Обрыв шлейфа ",
    50: "Закрыта крышка",
    56: 'Питание в норме  Адаптер "Дунай АД8" ',
    89: "Ответ на опрос Взят под охрану ",
    1: "Ответ на опрос Норма шлейфа ",
}

individual_results = {
    104: "нет сети 220в ",
    105: "Восстановление сети 220В ",
    106: "Аккумулятор норме ",
    107: "Аккумулятор разряжен ",
    108: "Открыта дверца ",
    109: "Закрыта дверца ",
    360: "Отстутствие 220в (Опрос)",
    361: "Востановление 220в (Опрос)",
    362: "Питание акумулятора в норме (Опрос)",
    363: "Акумулятор разряжен (Опрос)",
    364: "Открыта дверца (Опрос)",
    365: "Закрыта дверца (Опрос)",
    16149: "Проверка связи:  УСПЕШНО",
    16145: "Включен(о)",
    15649: "Версия микропрограммы [0011]",
    15646: "Версия микропрограммы [000F]",
    15645: "Версия микропрограммы [000D]",
    15644: "Версия микропрограммы [000C]",
    15643: "Версия микропрограммы [000B]",
    15650: "Версия микропрограммы [0012]",
    15651: "Версия микропрограммы [0013]",
    15652: "Версия микропрограммы [0014]",
    16146: "ППК выведен из режима Консервации",
}

user_ident = {
    2063 + i: "Идентификация ответственного %s" % str(i) for i in range(1, 129)
}
user_ident_2 = {
    2543 + i: "Идентификация ответственного %s" % str(i) for i in range(1, 129)
}
module_power_failed = {
    14351 + i: "Авария питания модуля %s" % str(i) for i in range(1, 33)
}
module_power_good = {
    14863 + i: "Питание модуля в норме %s" % str(i) for i in range(1, 33)
}
poll_module_power_good = {
    15120 + i: "Питание модуля в норме %s (Опрос)" % str(i) for i in range(33)
}

poll_module_connection_ok = {
    14095 + i: "Связь с адаптером востановлена %s (Опрос)" % str(i) for i in range(1, 33)
}

poll_module_tamper_ok = {
    13071 + i: "Закрыта крышка адаптера %s (Опрос)" % str(i) for i in range(1, 33)
}
poll_module_tamper_open = {
    12559 + i: "Открыта крышка адаптера %s (Опрос)" % str(i) for i in range(1, 33)
}

guard_on = { 16399 + i: "Взято под охрану %s" % str(i) for i in range(1, 1129) }
poll_guard_on = {
    16655 + i: "Група взято под охрану %s (Опрос)" % str(i) for i in range(1, 129)
}
guard_off = { 18447 + i: "Снятие группы %s" % str(i) for i in range(1, 129) }
poll_guard_off = {
    18703 + i: "Група знято с охраны %s (Опрос)" % str(i) for i in range(1, 129)
}

module_lost = { 13327 + i: "Нет связи с адаптером %s" % str(i) for i in range(1, 129) }
module_ok = {
    13839 + i: "Связь с адаптером востановлена %s" % str(i) for i in range(1, 129)
}

line_break = { 20495 + i: "Обрыв шлейфа %s" % str(i) for i in range(1, 129) }
line_break_128 = { 20975 + i: "Обрыв шлейфа %s" % str(i) for i in range(1, 129) }
poll_line_break = { 20751 + i: "Обрыв шлейфа %s (Опрос)" % str(i) for i in range(1, 129) }
poll_line_break_128 = { 21711 + i: "Обрыв шлейфа %s (Опрос)" % str(i) for i in range(1, 129) }
line_normal = { 22543 + i: "Норма шлейфа %s" % str(i) for i in range(1, 129) }
line_normal_128 = { 23023 + i: "Норма шлейфа %s" % str(i) for i in range(1, 129) }
line_normal_128_1 = { 23503 + i: "Норма шлейфа %s" % str(i) for i in range(1, 129) }
poll_line_normal = { 22799 + i: "Норма шлейфа %s (Опрос)" % str(i) for i in range(1, 129) }
poll_line_normal_128 = { 24239 + i: "Норма шлейфа %s (Опрос)" % str(i) for i in range(1, 129) }
poll_line_normal_128_1 = { 23281 + i: "Норма шлейфа группа %s (Опрос)" % str(i) for i in range(1, 129) }
poll_line_normal_128_2 = { 23759 + i: "Норма шлейфа группа %s (Опрос)" % str(i) for i in range(1, 129) }
poll_line_normal_128_3 = { 23983 + i: "Норма шлейфа группа %s (Опрос)" % str(i) for i in range(1, 129) }
poll_line_sc = { 28943 + i: "КЗ шлейфа %s (Опрос)" % str(i) for i in range(1, 129) }
line_sc = { 30735 + i: "КЗ шлейфа %s" % str(i) for i in range(1, 129) }
open_box = { 12303 + i: "Открыта крышка %s" % str(i) for i in range(1, 129) }
close_box = { 12815 + i: "Закрыта крышка %s" % str(i) for i in range(1, 129) }

merged_dict = {
    **individual_results,
    **user_ident,
    **module_power_failed,
    **module_power_good,
    **guard_on,
    **poll_guard_on,
    **guard_off,
    **poll_guard_off,
    **line_break,
    **poll_line_break,
    **line_normal,
    **poll_line_normal,
    **poll_line_sc,
    **line_sc,
    **open_box,
    **close_box,
    **module_lost,
    **module_ok,
    **line_break_128,
    **line_normal_128,
    **line_normal_128_1,
    **poll_module_power_good,
    **poll_module_tamper_ok,
    **poll_module_tamper_open,
    **poll_module_connection_ok,
    **poll_line_normal_128,
    **poll_line_normal_128_1,
    **poll_line_normal_128_2,
    **poll_line_break_128,
}


# json_result = (json.dumps(new_dict, ensure_ascii=False, indent=4).encode("utf8").decode("utf8"))
#
# with open('dict.json', 'r') as f:
#     f.read()
# json_result = (json.dumps(f, ensure_ascii=False, indent=4).encode("utf8").decode("utf8"))
# json.dumps('dict.json')
# with open("dict.json", "r", encoding="utf-8") as f:
#     msg_id_list = f.read()
#     msg_id_list = json.loads(msg_id_lis

class Generate_data():
    def __init__(self):
        self.merged_dict = {
            **individual_results,
            **user_ident,
            **module_power_failed,
            **module_power_good,
            **guard_on,
            **poll_guard_on,
            **guard_off,
            **poll_guard_off,
            **line_break,
            **poll_line_break,
            **line_normal,
            **poll_line_normal,
            **poll_line_sc,
            **line_sc,
            **open_box,
            **close_box,
            **module_lost,
            **module_ok,
            **line_break_128,
            **line_normal_128,
            **line_normal_128_1,
            **poll_module_power_good,
            **poll_module_tamper_ok,
            **poll_module_tamper_open,
            **poll_module_connection_ok,
            **poll_line_normal_128,
            **poll_line_normal_128_1,
            **poll_line_normal_128_2,
            **poll_line_break_128,
        }
