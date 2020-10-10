import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
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
class ExampleApp(QtWidgets.QMainWindow, design.Ui_Rcom_buffer, dicts.Generate_data):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py

        client = MongoClient("mongodb://localhost:27017/")
        self.db = client.DBClientsPPK
        self.diff_list = []
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(
            self.find_data
        )
        self.actionSave_to_html.triggered.connect(self.save_to_html)
        self.actionSave_to_txt.triggered.connect(self.save_to_txt)
        self.actionSave_to_markdown.triggered.connect(self.save_to_markdown)
        self.actionExit_2.triggered.connect(self.exit_app)
        self.progressBar.setMaximum(5000)
        self.events = []
        self.text_field = self.textEdit

    def save_to_txt(self):
        with open(datetime.strftime(datetime.now(), 'log_%H_%M_%S.txt'), 'w', encoding="utf8") as file:
            file.write(str(self.text_field.toPlainText()))

    def save_to_html(self):
        with open(datetime.strftime(datetime.now(), 'log_%H_%M_%S.html'), 'w', encoding="utf8") as file:
            file.write(str(self.text_field.toHtml()))

    def save_to_markdown(self):
        with open(datetime.strftime(datetime.now(), 'log_Markdown_%H_%M_%S.txt'), 'w', encoding="utf8") as file:
            file.write(str(self.text_field.toMarkdown()))

    def exit_app(self):
        sys.exit(0)

    def find_data(self):
        while True:
            try:
                QCoreApplication.processEvents()
                time.sleep(0.05)
                QCoreApplication.processEvents()
                self.data = self.db.Messages.find()
                QCoreApplication.processEvents()
                for msg in self.data:
                    if msg["_id"] not in self.diff_list:
                        id_msg = str(msg["id_msg"])
                        id_msg_keys = int(id_msg[id_msg.find("X") + 1:])
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
                            logger.info(self.text)
                            self.events.append(
                                str(msg["id_ppk"])
                                + " | "
                                + dicts.merged_dict[id_msg_keys]
                            )
                            self.diff_list.append(msg["_id"])
                            self.text_field.append(self.text)
                            self.progressBar.setValue(len(self.diff_list))
                            QCoreApplication.processEvents()
                            # print(msg)
                            time.sleep(0.02)
                            self.label_2.setText(
                                QCoreApplication.translate(
                                    "MainWindow",
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
                            logger.info(self.text)
                            self.progressBar.setValue(len(self.diff_list))
                            QCoreApplication.processEvents()
                            time.sleep(0.02)
                            self.diff_list.append(msg["_id"])
                            self.label_2.setText(
                                QCoreApplication.translate(
                                    "MainWindow",
                                    u"%s/5000" % str(len(self.diff_list) - 1),
                                    None,
                                )
                            )
                time.sleep(0.09)
                if len(self.diff_list) > 15000:
                    self.diff_list.clear()
                    # self.textBrowser.clear()
                    self.text_field.clear()
                if len(self.events) > 50000:
                    self.events.clear()
            except NameError as err:
                self.text_field.append(err)
                logger.debug(self.text)
            except KeyError:
                logger.debug(self.text)

    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if (
                directory
        ):  # не продолжать выполнение, если пользователь не выбрал директорию
            for file_name in os.listdir(directory):  # для каждого файла в директории
                self.listWidget.addItem(file_name)  # добавить файл в listWidget


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    sys.exit(0)


if __name__ == "__main__":  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()о запускаем функцию main()
