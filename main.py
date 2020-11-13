import asyncio
import os
import socket
import sys  # sys нужен для передачи argv в QApplication
from datetime import datetime

from PySide2 import QtWidgets
from PySide2.QtCore import QCoreApplication
from loguru import logger
from pymongo import MongoClient

import design  # Это наш конвертированный файл дизайна
import dicts

logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="1 days",
    compression="zip",
)


@logger.catch()
class Rcom_Buffer_Log(QtWidgets.QMainWindow, design.Ui_Rcom_buffer):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.01)
        self.sock.bind(("", 15555))
        self.addr = ('127.0.0.1', 15555)
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client.DBClientsPPK
        self.diff_list = []
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.run_async_main)
        self.actionSave_to_html.triggered.connect(self.save_to_html)
        self.actionSave_to_txt.triggered.connect(self.save_to_csv)
        self.actionSave_to_markdown.triggered.connect(self.save_to_markdown)
        self.actionClear_log.triggered.connect(self.clear_buffers)
        self.actionRemove_polls_from_buffer.triggered.connect(self.clear_poll_buffer)
        self.actionExit.triggered.connect(self.exit_app)
        self.max_val = 0
        self.events = []
        self.udp_data = ""
        self.text_field = self.textEdit
        self.text_field.setReadOnly(True)
        self.text_field.setUndoRedoEnabled(False)
        self.count = 1

    def save_to_csv(self):
        try:
            os.mkdir("log")
        except OSError as err:
            logger.debug(err)
        filename = datetime.strftime(datetime.now(), "log_%d_%m_%Y %H.%M.%S.csv")
        with open("log\\" + filename, "w", encoding="utf8") as file:
            file.write(str(self.text_field.toPlainText().replace(" |", ";")))

    def save_to_html(self):
        try:
            os.mkdir("log")
        except OSError as err:
            logger.debug(err)
        filename = datetime.strftime(datetime.now(), "log_%d/%m/%Y %H.%M.%S.html")
        with open("log\\" + filename, "w", encoding="utf8") as file:
            file.write(str(self.text_field.toHtml()))

    def save_to_markdown(self):
        try:
            os.mkdir("log")
        except OSError as err:
            logger.debug(err)
        filename = datetime.strftime(datetime.now(), "log_%d/%m/%Y %H.%M.%S.txt")
        with open("log\\" + filename, "w", encoding="utf8") as file:
            file.write(str(self.text_field.toMarkdown()))

    def clear_buffers(self):
        self.text_field.clear()
        self.diff_list.clear()
        self.events.clear()
        self.count = 0

    def clear_poll_buffer(self):
        self.data = self.db.Messages.find()
        self.collection_Messages = self.db.Messages
        for self.msg in self.data:
            id_msg = str(self.msg["id_msg"])
            self.id_msg_keys = int(id_msg[id_msg.find("X") + 1 :])
            if self.id_msg_keys in dicts.poll_dict.keys():
                dict_msg = {"id_msg": id_msg}
                self.collection_Messages.delete_one(dict_msg)

    def exit_app(self):
        sys.exit(0)

    async def udp_server(self):
        self.addr_list = []
        while True:
            try:
                self.udp_data, self.addr = self.sock.recvfrom(10240)
                self.result = self.udp_data.decode('utf8').split(',')
                if self.result[0] == 'clear_poll_buffer':
                    self.clear_poll_buffer()
                    logger.info('Clear ok')
                if self.addr not in self.addr_list:
                    self.addr_list.append(self.addr)
                    for ip in self.addr_list:
                        logger.info('connection from {0}'.format(ip))

            except socket.timeout:
                await asyncio.sleep(1)
            except ConnectionResetError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue
            except OSError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue


    async def send_udp(self):
        print(self.udp_data)
        await asyncio.sleep(0.01)
        for self.ip in self.addr_list:
            logger.info(self.ip)
            try:
                await asyncio.sleep(0.03)
                self.sock.sendto(
                    (
                        ("buffer_count, {0}, {1}\n")
                            .format(
                            self.db.Messages.estimated_document_count(),
                            self.find_progress_bar_max(
                                self.db.Messages.estimated_document_count() - 1
                            ),
                        )
                            .encode("utf8")
                    ),
                    (self.ip[0], self.ip[1]),
                )
                await asyncio.sleep(0.03)
                self.sock.sendto(
                    (
                        ("text_field, {1}")
                            .format(0, self.text)
                            .encode("utf8")
                    ),
                    (self.addr[0], self.addr[1]),
                )

            except socket.timeout:
                await asyncio.sleep(1)
            except ConnectionResetError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue
            except OSError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue
            except AttributeError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue

    def dup_count(self):
        dup = self.events.count(
            str(self.msg["id_ppk"]) + " | " + dicts.merged_dict[self.id_msg_keys]
        )
        return dup

    async def write_msg_in_window_if_msg_in_dict(self):
        self.text = "{0} | {1} | ППК: {2} | Повторних | {3} | {4}".format(
            str(self.count),
            datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"),
            str(self.msg["id_ppk"]),
            str(self.dup_count()),
            dicts.merged_dict[self.id_msg_keys],
        )

    async def write_msg_in_window_if_msg_not_in_dict(self):
        self.text = "| msg count {0} | {1} | {2}".format(
            str(len(self.diff_list)),
            datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"),
            str(self.msg),
        )

    def find_progress_bar_max(self, value):
        if value >= self.max_val:
            self.max_val = value
        return self.max_val

    async def buffer_count(self):
        self.label_4.setText(
            QCoreApplication.translate(
                "Rcom_buffer",
                u"%s/%s"
                % (
                    self.db.Messages.estimated_document_count(),
                    self.find_progress_bar_max(
                        self.db.Messages.estimated_document_count() - 1
                    ),
                ),
                None,
            )
        )
        for self.ip in self.addr_list:
            try:
                self.sock.sendto(
                    (
                        ("buffer_count, {0}, {1}\n")
                        .format(
                            self.db.Messages.estimated_document_count(),
                            self.find_progress_bar_max(
                                self.db.Messages.estimated_document_count() - 1
                            ),
                        )
                        .encode("utf8")
                    ),
                    (self.ip[0], self.ip[1]),
                )
            except socket.timeout:
                await asyncio.sleep(1)
            except ConnectionResetError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue
            except OSError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue

    async def update_window(self):
        while True:
            QCoreApplication.processEvents()
            await asyncio.sleep(0.03)

    def progressbar_2_get_maximum(self):
        self.progressBar_2.setValue(self.db.Messages.estimated_document_count())


    async def set_progressbar_2_maximum(self):
        self.progressBar_2.setMaximum(
            self.find_progress_bar_max(
                self.find_progress_bar_max(self.db.Messages.estimated_document_count())
            )
        )


    async def get_data_from_db_and_write_to_main_window(self):
        self.text_field.append(
            "Count | Date | PPK number | Number of dublicates | Message"
        )
        while True:
            await asyncio.sleep(0.11)
            try:
                await asyncio.sleep(1)
                await self.buffer_count()
                self.data = self.db.Messages.find()
                for self.msg in self.data:
                    await asyncio.sleep(0.05)
                    if self.msg["_id"] not in self.diff_list:
                        await asyncio.sleep(0.05)
                        id_msg = str(self.msg["id_msg"])
                        self.id_msg_keys = int(id_msg[id_msg.find("X") + 1 :])
                        if self.id_msg_keys in dicts.merged_dict.keys():
                            await self.write_msg_in_window_if_msg_in_dict()
                            self.events.append(
                                str(self.msg["id_ppk"])
                                + " | "
                                + dicts.merged_dict[self.id_msg_keys]
                            )
                            self.diff_list.append(self.msg["_id"])

                            self.text_field.append(self.text)
                            await asyncio.sleep(0.03)
                            # await self.send_udp()
                            for self.ip in self.addr_list:
                                try:
                                    self.sock.sendto(
                                        (
                                            ("text_field, {1}")
                                            .format(0, self.text)
                                            .encode("utf8")
                                        ),
                                        (self.ip[0], self.ip[1]),
                                    )
                                except socket.timeout:
                                    await asyncio.sleep(1)
                                except ConnectionResetError as err:
                                    logger.debug(err)
                                    await asyncio.sleep(1)
                                    continue
                                except OSError as err:
                                    logger.debug(err)
                                    await asyncio.sleep(1)
                                    continue
                                except AttributeError as err:
                                    logger.debug(err)
                                    await asyncio.sleep(1)
                                    continue

                            await self.set_progressbar_2_maximum()

                            self.progressbar_2_get_maximum()

                            self.count += 1

                        else:
                            await self.write_msg_in_window_if_msg_not_in_dict()
                            logger.info(self.msg)
                            self.text_field.append(self.text)
                            self.diff_list.append(self.msg["_id"])
                            self.count += 1
                if len(self.diff_list) >= 5000:
                    self.diff_list.clear()
                if len(self.events) > 50000:
                    self.save_to_csv()
                    self.clear_buffers()
            except NameError as err:
                self.text_field.append(err)
                logger.debug(self.text)
            except KeyError:
                logger.debug(self.text)
            except AttributeError as err:
                logger.debug(err)
                await asyncio.sleep(1)
                continue

    async def async_main(self):
        task1 = asyncio.create_task(self.get_data_from_db_and_write_to_main_window())
        task2 = asyncio.create_task(self.update_window())
        task3 = asyncio.create_task(self.udp_server())
        # task4 = asyncio.create_task(self.send_udp())
        await asyncio.gather(task1, task2, task3)

    def run_async_main(self):
        asyncio.run(self.async_main())


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Rcom_Buffer_Log()  # Создаём объект класса Rcom_Buffer_Log
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    sys.exit(window.exit_app)


if __name__ == "__main__":  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
