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

    def save_to_txt(self):
        with open(
            datetime.strftime(datetime.now(), "log_%H_%M_%S.txt"), "w", encoding="utf8"
        ) as file:
            file.write(str(self.text_field.toPlainText()))

    def save_to_html(self):
        with open(
            datetime.strftime(datetime.now(), "log_%H_%M_%S.html"), "w", encoding="utf8"
        ) as file:
            file.write(str(self.text_field.toHtml()))

    def save_to_markdown(self):
        with open(
            datetime.strftime(datetime.now(), "log_Markdown_%H_%M_%S.txt"),
            "w",
            encoding="utf8",
        ) as file:
            file.write(str(self.text_field.toMarkdown()))

    def clear_buffers(self):
        self.text_field.clear()

    def exit_app(self):
        sys.exit(0)

    def find_progress_bar_max(self, value):
        if value >= self.max_val:
            self.max_val = value
        return self.max_val

    def find_data(self):
        self.text_field.append("Program start")
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
                self.progressBar_2.setMaximum(
                    self.find_progress_bar_max(
                        self.find_progress_bar_max(
                            self.db.Messages.estimated_document_count()
                        )
                    )
                )
                QCoreApplication.processEvents()
                self.data = self.db.Messages.find()
                QCoreApplication.processEvents()
                for msg in self.data:
                    if msg["_id"] not in self.diff_list:
                        id_msg = str(msg["id_msg"])
                        id_msg_keys = int(id_msg[id_msg.find("X") + 1 :])
                        if id_msg_keys in dicts.merged_dict.keys():
                            self.text = (
                                "| msg count "
                                + str(len(self.diff_list))
                                + " | "
                                + str(
                                    self.events.count(
                                        str(msg["id_ppk"])
                                        + " | "
                                        + dicts.merged_dict[id_msg_keys]
                                    )
                                )
                                + " | "
                                + datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                                + " | Номер ППК | "
                                + str(msg["id_ppk"])
                                + " | "
                                + dicts.merged_dict[id_msg_keys]
                            )
                            # logger.info(self.text)
                            self.events.append(
                                str(msg["id_ppk"])
                                + " | "
                                + dicts.merged_dict[id_msg_keys]
                            )
                            self.diff_list.append(msg["_id"])
                            self.text_field.append(self.text)
                            self.progressBar.setValue(len(self.diff_list))
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

                        else:
                            self.text = (
                                "| msg count "
                                + str(len(self.diff_list))
                                + " | "
                                + datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
                                + " | "
                                + str(msg)
                            )
                            logger.info(msg)
                            self.progressBar.setValue(len(self.diff_list))
                            self.text_field.append(self.text)
                            QCoreApplication.processEvents()
                            time.sleep(0.01)
                            self.diff_list.append(msg["_id"])
                            self.label_2.setText(
                                QCoreApplication.translate(
                                    "Rcom_buffer",
                                    u"%s/5000" % str(len(self.diff_list) - 1),
                                    None,
                                )
                            )

                time.sleep(0.09)
                if len(self.diff_list) >= 5000:
                    self.diff_list.clear()
                if len(self.events) > 500000:
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
    sys.exit(0)


if __name__ == "__main__":  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()о запускаем функцию main()
