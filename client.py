import asyncio
import os
import socket
import sys  # sys нужен для передачи argv в QApplication
from datetime import datetime

import yaml
from PySide2 import QtWidgets
from PySide2.QtCore import QCoreApplication
from loguru import logger

import design  # Это наш конвертированный файл дизайна

logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="1 days",
    compression="zip",
)


try:
    with open('rcom_client.yaml') as f:
        yaml_config = yaml.safe_load(f)
except FileNotFoundError:
    IP = "127.0.0.1"
    PORT = 15555


    to_yaml = {'IP': IP,
               'PORT': PORT,
               }

    with open('rcom_client.yaml', 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style=False)

    with open('rcom_client.yaml') as f:
        yaml_config = yaml.safe_load(f)

@logger.catch()
class Rcom_Buffer_Log(QtWidgets.QMainWindow, design.Ui_Rcom_buffer):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.01)
        # self.sock.bind(("", 47585))
        print(yaml_config['IP'], yaml_config['PORT'])
        self.addr = (yaml_config['IP'], yaml_config['PORT'])
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

    def clear_poll_buffer(self):
        self.sock.sendto(
            (("clear_poll_buffer").encode("utf8")), (self.addr[0], self.addr[1]),
        )

    def exit_app(self):
        self.sock.close()
        sys.exit(0)

    async def udp_server(self):
        while True:
            try:
                self.sock.sendto(
                    (("ok").encode("utf8")), (self.addr[0], self.addr[1]),
                )
                self.udp_data, self.addr = self.sock.recvfrom(10240)
                print(self.addr[0])
                print(self.udp_data.decode('utf8'))
                self.result = self.udp_data.decode('utf8').split(',')
                print(self.result[0])
                self.sock.sendto(
                    (("ok").encode("utf8")), (self.addr[0], self.addr[1]),
                )
                await asyncio.sleep(0.01)
                if self.result[0] == 'buffer_count':
                    self.current_progressbar_value = int(self.result[1])
                    self.max_progressbar_value = int(self.result[2])
                    await self.buffer_count()
                    self.progressBar_2.setValue(int(self.current_progressbar_value))
                    self.progressBar_2.setMaximum(int(self.max_progressbar_value))
                if self.result[0] == 'text_field':
                    self.text_window = self.result[1]

                    self.text_field.append(self.text_window)

            except socket.timeout:
                await asyncio.sleep(0.1)
            except ConnectionResetError as err:
                print(err)
                await asyncio.sleep(5.1)
                continue
            except OSError as err:
                print(err)
                self.sock.close()
                await asyncio.sleep(5.1)
                continue



    async def buffer_count(self):
        self.label_4.setText(QCoreApplication.translate("Rcom_buffer", u"{0}/{1}".format(self.current_progressbar_value, self.max_progressbar_value), None))



    async def update_window(self):
        while True:
            QCoreApplication.processEvents()
            await asyncio.sleep(0.03)



    async def get_data_from_db_and_write_to_main_window(self):
        self.text_field.append(
            "Count | Date | PPK number | Number of dublicates | Message"
        )
        while True:
            try:
                await asyncio.sleep(1)

            except NameError as err:
                self.text_field.append(err)
                logger.debug(self.text)
            except KeyError:
                logger.debug(self.text)
            except AttributeError as err:
                logger.debug(err)

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


 # Если мы запускаем файл напрямую, а не импортируем
main()  # то запускаем функцию main()
