import os
import socket
import sys  # sys нужен для передачи argv в QApplication
import time
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

        client = MongoClient("mongodb://localhost:27017/")
        self.db = client.DBClientsPPK
        self.diff_list = []
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.find_data)
        self.actionSave_to_html.triggered.connect(self.save_to_html)
        self.actionSave_to_txt.triggered.connect(self.save_to_txt)
        self.actionSave_to_markdown.triggered.connect(self.save_to_markdown)
        self.actionClear_log.triggered.connect(self.clear_buffers)
        self.actionExit.triggered.connect(self.exit_app)
        self.max_val = 0
        self.progressBar.setMaximum(5000)
        self.events = []
        self.text_field = self.textEdit
        self.count = 0

    def save_to_txt(self):
        try:
            os.mkdir("log")
        except OSError as err:
            print(err)
        filename = datetime.strftime(datetime.now(), "log_%d_%m_%Y %H.%M.%S.csv")
        with open("log\\" + filename, "w", encoding="utf8") as file:
            file.write(str(self.text_field.toPlainText().replace(" |", ";")))

    def save_to_html(self):
        try:
            os.mkdir("log")
        except OSError as err:
            print(err)
        filename = datetime.strftime(datetime.now(), "log_%d/%m/%Y %H.%M.%S.html")
        with open("log\\" + filename, "w", encoding="utf8") as file:
            file.write(str(self.text_field.toHtml()))

    def save_to_markdown(self):
        try:
            os.mkdir("log")
        except OSError as err:
            print(err)
        filename = datetime.strftime(datetime.now(), "log_%d/%m/%Y %H.%M.%S.txt")
        with open("log\\" + filename, "w", encoding="utf8") as file:
            file.write(str(self.text_field.toMarkdown()))

    def clear_buffers(self):
        self.text_field.clear()
        self.diff_list.clear()
        self.count = 0

    def exit_app(self):
        sys.exit(0)

    def send_udp(self, udp_data):
        self.udp_data = bytes(udp_data, encoding='utf8')
        self.UDP_IP = "10.32.2.49"
        self.UDP_PORT = 27009
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.sendto((self.udp_data), (self.UDP_IP, self.UDP_PORT))

    def write_msg_in_window_if_msg_in_dict(self):
        self.text = (
                str(self.count)
                + " | "
                + datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                + " | ППК "
                + str(self.msg["id_ppk"])
                + " | Повторних "
                + str(
            self.events.count(
                str(self.msg["id_ppk"])
                + " | "
                + dicts.merged_dict[self.id_msg_keys]
            )
        )
                + " | "
                + dicts.merged_dict[self.id_msg_keys]
        )

    def write_msg_in_window_if_msg_not_in_dict(self):
        self.text = (
                "| msg count "
                + str(len(self.diff_list))
                + " | "
                + datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                + " | "
                + str(self.msg)
        )

    def find_progress_bar_max(self, value):
        if value >= self.max_val:
            self.max_val = value
        return self.max_val

    def find_data(self):
        self.text_field.append(
            "Count | Date | PPK number | Number of dublicates | Message"
        )
        while True:
            try:
                QCoreApplication.processEvents()
                time.sleep(0.01)
                self.label_4.setText(
                    QCoreApplication.translate(
                        "Rcom_buffer",
                        u"%s/%s"
                        % (
                            self.db.Messages.estimated_document_count(),
                            self.find_progress_bar_max(
                                self.db.Messages.estimated_document_count()
                            ),
                        ),
                        None,
                    )
                )

                QCoreApplication.processEvents()
                self.data = self.db.Messages.find()
                QCoreApplication.processEvents()
                for self.msg in self.data:
                    if self.msg["_id"] not in self.diff_list:
                        id_msg = str(self.msg["id_msg"])
                        self.id_msg_keys = int(id_msg[id_msg.find("X") + 1 :])
                        if self.id_msg_keys in dicts.merged_dict.keys():
                            self.write_msg_in_window_if_msg_in_dict()
                            self.send_udp(self.text)
                            self.events.append(
                                str(self.msg["id_ppk"])
                                + " | "
                                + dicts.merged_dict[self.id_msg_keys]
                            )
                            self.diff_list.append(self.msg["_id"])
                            self.text_field.append(self.text)
                            self.progressBar.setValue(len(self.diff_list))
                            self.progressBar_2.setMaximum(
                                self.find_progress_bar_max(
                                    self.find_progress_bar_max(
                                        self.db.Messages.estimated_document_count()
                                    )
                                )
                            )
                            self.progressBar_2.setValue(
                                self.db.Messages.estimated_document_count()
                            )
                            QCoreApplication.processEvents()
                            # print(msg)
                            time.sleep(0.01)
                            self.label_2.setText(
                                QCoreApplication.translate(
                                    "Rcom_buffer",
                                    u"%s/5000" % str(len(self.diff_list) - 1),
                                    None,
                                )
                            )
                            self.count += 1
                        else:
                            self.write_msg_in_window_if_msg_not_in_dict()
                            logger.info(self.msg)
                            self.progressBar.setValue(len(self.diff_list))
                            self.text_field.append(self.text)
                            QCoreApplication.processEvents()
                            time.sleep(0.01)
                            self.diff_list.append(self.msg["_id"])
                            self.label_2.setText(
                                QCoreApplication.translate(
                                    "Rcom_buffer",
                                    u"%s/5000" % str(len(self.diff_list) - 1),
                                    None,
                                )
                            )
                            self.count += 1
                time.sleep(0.09)
                if len(self.diff_list) >= 5000:
                    self.diff_list.clear()
                if len(self.events) > 5000000:
                    self.events.clear()
            except NameError as err:
                self.text_field.append(err)
                logger.debug(self.text)
            except KeyError:
                logger.debug(self.text)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Rcom_Buffer_Log()  # Создаём объект класса Rcom_Buffer_Log
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    sys.exit(window.exit_app())


if __name__ == "__main__":  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()о запускаем функцию main()
