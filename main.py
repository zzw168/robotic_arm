import os
import socket
import sys
import time

import yaml
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QMenu
import json

import pynput
# ...省略部分
import base64
from icon import img
import os

from Robot_Ui import Ui_MainWindow

send_data = {"startButton": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["startButton"]},  # 启动按钮
             "stopButton": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["stopButton"]},  # 停止按钮
             "actionStop": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionStop"]},  # 立即停止
             "actionPause": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionPause"]},  # 暂停当前动作
             "actionSingleCycle": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                                   "cmdData": ["actionSingleCycle"]},
             # 进入单循环
             "clearAlarmRunNext": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                                   "cmdData": ["clearAlarmRunNext"]},
             # 清除报警后运行下一条指令
             "clearAlarmContinue": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                                    "cmdData": ["clearAlarmContinue"]},
             # 清除报警后继续运行条指令
             "modifyGSPD": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["modifyGSPD", "10"]},
             # 全局速度修改:("d1":速度)
             "rewriteData": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                             "cmdData": ["rewriteData", "800", "6", "0"]},
             # 数据修改:("d1":addrs,"d2":value,"d3":savable)
             "rewriteDataList": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                                 "cmdData": ["rewriteDataList", "800", "6", "0", "0", "0", "0", "0", "-60000",
                                             "0"]},
             # 800，6，0，左右，前后， 上下，摄像头左右旋转，摄像头上下，镜头旋转
             # 数据块修改:("d1":addrs,"d2":length,"d3":savable,"d4","d5","d6","d7"...)
             "modifyAccDec": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["clearAlarmContinue"]},
             # 路径加减速修改:("d1":加速时间，"d2":减速时间),时间数据= 时间*1000
             "switchTool": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["switchTool"]},
             # 切换工具编号
             "modifyTool": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["modifyTool"]},
             # 修改工具信息
             "switchCoordinate": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["switchCoordinate"]},
             # 切换工作台
             }


def FrontBack():
    table = ui.tableWidget
    num = table.currentRow()
    item = QTableWidgetItem(str(ui.Slider_FrontBack.value() * 1))
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(num, 5, item)


def UpDown():
    table = ui.tableWidget
    num = table.currentRow()
    item = QTableWidgetItem(str(ui.Slider_UpDown.value() * 1))
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(num, 6, item)


def RightLeft():
    table = ui.tableWidget
    num = table.currentRow()
    item = QTableWidgetItem(str(ui.Slider_RightLeft.value() * -1))
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(num, 4, item)


def HeadRotate():
    table = ui.tableWidget
    num = table.currentRow()
    item = QTableWidgetItem(str(ui.Slider_HeadRotate.value() * 1))
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(num, 7, item)


def HeadUpDown():
    table = ui.tableWidget
    num = table.currentRow()
    item = QTableWidgetItem(str(ui.Slider_HeadUpDown.value() * 1))
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(num, 8, item)


def lensRotate():
    table = ui.tableWidget
    num = table.currentRow()
    item = QTableWidgetItem(str(ui.Slider_lensRotate.value() * 1))
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(num, 9, item)


def table_clicked():
    table = ui.tableWidget
    row = table.currentRow()
    n = table.item(row, 4).text()

    if (n == '') or not (n.isdigit() or (n[0] == '-' and n[1:].isdigit())):
        return
    n = int(n)
    ui.Slider_RightLeft.setValue(int(n / -1))

    n = table.item(row, 5).text()
    if (n == '') or not (n.isdigit() or (n[0] == '-' and n[1:].isdigit())):
        return
    n = int(n)
    ui.Slider_FrontBack.setValue(int(n / 1))

    n = table.item(row, 6).text()
    if (n == '') or not (n.isdigit() or (n[0] == '-' and n[1:].isdigit())):
        return
    n = int(n)
    ui.Slider_UpDown.setValue(int(n / 1))

    n = table.item(row, 7).text()
    if (n == '') or not (n.isdigit() or (n[0] == '-' and n[1:].isdigit())):
        return
    n = int(n)
    ui.Slider_HeadRotate.setValue(int(n / 1))

    n = table.item(row, 8).text()
    if (n == '') or not (n.isdigit() or (n[0] == '-' and n[1:].isdigit())):
        return
    n = int(n)
    ui.Slider_HeadUpDown.setValue(int(n / 1))

    n = table.item(row, 9).text()
    if (n == '') or not (n.isdigit() or (n[0] == '-' and n[1:].isdigit())):
        return
    n = int(n)
    ui.Slider_lensRotate.setValue(int(n / 1))


class MyUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super(MyUi, self).setupUi(MainWindow)

        tb = self.tableWidget
        tb.horizontalHeader().resizeSection(0, 10)
        tb.horizontalHeader().resizeSection(1, 80)
        tb.setColumnHidden(3, True)
        tb.horizontalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb.verticalHeader().setStyleSheet("QHeaderView::section{background:rgb(245,245,245);}")
        tb.clicked.connect(table_clicked)

        tb.setContextMenuPolicy(Qt.CustomContextMenu)
        tb.customContextMenuRequested.connect(self.generateMenu)

        self.Slider_FrontBack.valueChanged.connect(FrontBack)
        self.Slider_UpDown.valueChanged.connect(UpDown)
        self.Slider_RightLeft.valueChanged.connect(RightLeft)
        self.Slider_HeadRotate.valueChanged.connect(HeadRotate)
        self.Slider_HeadUpDown.valueChanged.connect(HeadUpDown)
        self.Slider_lensRotate.valueChanged.connect(lensRotate)

    def generateMenu(self, pos):
        tb = self.tableWidget

        menu = QMenu()
        item1 = menu.addAction("刷新")
        item2 = menu.addAction("删除")
        item3 = menu.addAction("插入")
        screenPos = tb.mapToGlobal(pos)

        action = menu.exec(screenPos)
        if action == item1:
            Flash_Thead.start()
        if action == item2:
            # del_host()
            num = tb.rowCount()
            if num != 0:
                p = tb.currentRow()
                for i in range(p, num - 1):
                    # print('%d' % i)
                    for j in range(0, tb.columnCount()):
                        if j == 0:
                            cb = QCheckBox()
                            cb.setStyleSheet('QCheckBox{margin:6px};')
                            cb.setChecked(tb.cellWidget(i + 1, j).isChecked())
                            tb.setCellWidget(i, j, cb)
                        else:
                            item = QTableWidgetItem(tb.item(i + 1, j).text())
                            item.setTextAlignment(Qt.AlignCenter)
                            tb.setItem(i, j, item)
                tb.setRowCount(num - 1)
        if action == item3:
            table = ui.tableWidget
            num = table.rowCount()
            table.setRowCount(num + 1)
            row = table.currentRow()
            for r in range(num, row, -1):
                cb = QCheckBox()
                cb.setStyleSheet('QCheckBox{margin:6px};')
                table.setCellWidget(r, 0, cb)
                table.cellWidget(r, 0).setChecked(table.cellWidget(r - 1, 0).isChecked())
                for i in range(1, table.columnCount()):
                    item = QTableWidgetItem(table.item(r - 1, i).text())
                    item.setTextAlignment(Qt.AlignCenter)
                    # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                    table.setItem(r, i, item)


class FlashThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(FlashThead, self).__init__()

    def run(self) -> None:
        global host_list1
        global host_list2
        global host_list3
        global d_time1
        global d_time2
        global d_time3
        global ischecked1
        global ischecked2
        global ischecked3
        file = "./Robot.yml"
        if os.path.exists(file):
            f = open(file, 'r', encoding='utf-8')
            f_ = yaml.safe_load(f)
            d_time1 = f_['d_time']
            d_time2 = f_['d_time2']
            d_time3 = f_['d_time3']
            host_list1 = f_['Tasks']
            host_list2 = f_['Tasks2']
            host_list3 = f_['Tasks3']
            ischecked1 = f_['ischecked']
            ischecked2 = f_['ischecked2']
            ischecked3 = f_['ischecked3']
            self._signal.emit('ok')
            f.close()
        else:
            print("文件不存在")


def flashsignal_accept(message):
    print(message)
    global host_list
    global d_time
    global ischecked
    table = ui.tableWidget
    num = 0
    if ui.radioButton_1.isChecked():
        host_list = host_list1
        d_time = d_time1
        ischecked = ischecked1
    elif ui.radioButton_2.isChecked():
        host_list = host_list2
        d_time = d_time2
        ischecked = ischecked2
    elif ui.radioButton_3.isChecked():
        host_list = host_list3
        d_time = d_time3
        ischecked = ischecked3
    else:
        host_list = host_list1
        d_time = d_time1
        ischecked = ischecked1
    for task in host_list:
        table.setRowCount(num + 1)
        cb = QCheckBox()
        cb.setStyleSheet('QCheckBox{margin:6px};')
        table.setCellWidget(num, 0, cb)
        if ischecked[num] == '1':
            table.cellWidget(num, 0).setChecked(True)
        else:
            table.cellWidget(num, 0).setChecked(False)
        item = QTableWidgetItem(str(d_time[num]))
        item.setTextAlignment(Qt.AlignCenter)
        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
        table.setItem(num, 10, item)

        for i in range(1, len(task['cmdData'])):
            item = QTableWidgetItem(str(task['cmdData'][i]))
            item.setTextAlignment(Qt.AlignCenter)
            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
            table.setItem(num, i, item)

        num += 1
    # print(host_list)
    ui.lineEdit_speed.setText(speed)


def deal_yaml():
    global host_list
    global d_time
    global speed
    file = "./Robot.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        f_ = yaml.safe_load(f)
        d_time = f_['d_time']
        host_list = f_['Tasks']
        ischecked = f_['ischecked']
        speed = f_['speed']
        ui.lineEdit_speed.setText(speed)
        modifyGSPD()

        ui.radioButton_1.setChecked(True)

        f.close()
        table = ui.tableWidget
        num = 0
        for task in host_list:
            table.setRowCount(num + 1)
            cb = QCheckBox()
            cb.setStyleSheet('QCheckBox{margin:6px};')
            table.setCellWidget(num, 0, cb)
            if ischecked[num] == '1':
                table.cellWidget(num, 0).setChecked(True)
            item = QTableWidgetItem(str(d_time[num]))
            item.setTextAlignment(Qt.AlignCenter)
            # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
            table.setItem(num, 10, item)

            for i in range(1, len(task['cmdData'])):
                item = QTableWidgetItem(str(task['cmdData'][i]))
                item.setTextAlignment(Qt.AlignCenter)
                # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
                table.setItem(num, i, item)

            num += 1
        # print(host_list)
    else:
        print("文件不存在")


def save_host():
    global host_list
    global d_time
    table = ui.tableWidget
    num = table.rowCount()
    colnum = table.columnCount()
    if num == 0:
        return
    host_list = []
    host = []
    d_time = []
    ischecked = []
    for i in range(0, num):
        host.append('rewriteDataList')
        d_time.append(table.item(i, 10).text())
        if table.cellWidget(i, 0).isChecked():
            ischecked.append("1")
        else:
            ischecked.append("0")
        for j in range(1, colnum - 1):
            # host.append(table.item(i, j).text())
            host.append("0" if table.item(i, j).text() == "" else table.item(i, j).text())

        h = {'dsID': 'HCRemoteMonitor', 'cmdType': 'command', 'cmdData': host}
        host_list.append(h)
        host = []
    print(host_list)

    file = "./Robot.yml"
    if os.path.exists(file):
        f = open(file, 'r', encoding='utf-8')
        robot_conf = yaml.safe_load(f)
        f.close()
        if ui.radioButton_2.isChecked():
            robot_conf['Tasks2'] = host_list
            robot_conf['d_time2'] = d_time
            robot_conf['ischecked2'] = ischecked
        elif ui.radioButton_3.isChecked():
            robot_conf['Tasks3'] = host_list
            robot_conf['d_time3'] = d_time
            robot_conf['ischecked3'] = ischecked
        else:
            robot_conf['Tasks'] = host_list
            robot_conf['d_time'] = d_time
            robot_conf['ischecked'] = ischecked
        print(robot_conf)

        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(robot_conf, f, allow_unicode=True)
            ui.textBrowser_msg.setText("保存服务器完成")


def add_host():
    table = ui.tableWidget
    num = table.rowCount()
    table.setRowCount(num + 1)
    cb = QCheckBox()
    cb.setStyleSheet('QCheckBox{margin:6px};')
    table.setCellWidget(num, 0, cb)
    for i in range(1, table.columnCount()):
        item = QTableWidgetItem(table.item(num - 1, i).text())
        item.setTextAlignment(Qt.AlignCenter)
        # item.setFlags(QtCore.Qt.ItemFlag(63))   # 单元格可编辑
        table.setItem(num, i, item)


class CmdThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(CmdThead, self).__init__()
        self.run_flg = ''

    def run(self) -> None:
        try:
            # 1.创建socket
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 2. 链接服务器
            server_addr = ("192.168.4.4", 9760)
            tcp_socket.connect(server_addr)

            tcp_socket.send(json.dumps(self.run_flg).encode("gbk"))

            # 接收响应
            response = tcp_socket.recv(4096)

            # 打印响应
            print(response.decode('utf-8'))
            self._signal.emit(response.decode('utf-8'))

            # 4. 关闭套接字
            tcp_socket.close()
        except:
            print("服务链接出错")
            self._signal.emit("服务链接出错")


class UpdateThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(UpdateThead, self).__init__()
        self.run_flg = False
        self.once_flg = False
        self.stop_flg = False
        self.next_flg = False

    def run(self) -> None:
        global host_list
        # print(host_list)
        table = ui.tableWidget

        while True:
            if self.run_flg:
                try:
                    num = table.rowCount()
                    for i in range(0, num):
                        if table.cellWidget(i, 0).isChecked() and self.run_flg:
                            print("%s %s" % (i, table.item(i, 10).text()))
                            # update(i)
                            self._signal.emit("%d" % i)
                            for j in range(0, int(table.item(i, 10).text())):
                                time.sleep(1)
                                if self.next_flg:
                                    self.next_flg = False
                                    break
                            while self.stop_flg:
                                # time.sleep(1)
                                pass
                except:
                    print("列表出错")
                    self._signal.emit("列表出错")
            if self.one_flg:
                self.run_flg = False
                break


def signal_accept(message):
    print(message)
    print(type(message))
    if message.isdigit():
        message = int(message)
        table = ui.tableWidget
        num = table.columnCount()
        for j in range(0, table.rowCount()):
            if j == message:
                if table.item(j, 1).background().color() != QColor(200, 100, 200):
                    for i in range(1, num):
                        table.item(j, i).setBackground(QBrush(QColor(200, 100, 200)))
            else:
                if table.item(j, 1).background().color() != QColor(255, 255, 255):
                    for i in range(1, num):
                        table.item(j, i).setBackground(QBrush(QColor(255, 255, 255)))
    else:
        ui.textBrowser.append(message)
        if "ok" in message:
            if "startButton" in message:
                ui.textBrowser_msg.append("启动成功")
            elif "stopButton" in message:
                ui.textBrowser_msg.append("停止成功")
            elif "modifyGSPD" in message:
                ui.textBrowser_msg.append("换速成功")


def start():
    ui.textBrowser_msg.setText('')
    Cmd_Thead.run_flg = send_data["startButton"]
    Cmd_Thead.start()


def stop():
    ui.textBrowser_msg.setText('')
    Cmd_Thead.run_flg = send_data["stopButton"]
    Cmd_Thead.start()


def modifyGSPD():
    ui.textBrowser_msg.setText('')
    Cmd_Thead.run_flg = send_data["modifyGSPD"]
    Cmd_Thead.run_flg["cmdData"][1] = ui.lineEdit_speed.text()
    print(Cmd_Thead.run_flg)
    Cmd_Thead.start()


def update(num):
    Cmd_Thead.run_flg = send_data["rewriteDataList"]
    table = ui.tableWidget
    colnum = table.columnCount()
    for i in range(1, 3):
        Cmd_Thead.run_flg["cmdData"][i] = table.item(num, i).text()
    for i in range(4, colnum - 1):
        Cmd_Thead.run_flg["cmdData"][i] = "%s%s" % (table.item(num, i).text(), '000')
    print(Cmd_Thead.run_flg)
    Cmd_Thead.start()


def updateonce():
    Update_Thead.run_flg = True
    Update_Thead.one_flg = True
    Update_Thead.start()
    # ui.pushButton_update.setText("停止循环")


def updatelist():
    Update_Thead.run_flg = not (Update_Thead.run_flg)
    Update_Thead.one_flg = False
    Update_Thead.start()
    if Update_Thead.run_flg:
        ui.pushButton_update.setText("停止循环")
    else:
        ui.pushButton_update.setText("连续循环")


def sel_all():
    table = ui.tableWidget
    num = table.rowCount()
    for i in range(0, num):
        if ui.checkBox_selectall.isChecked():
            table.cellWidget(i, 0).setChecked(True)
        else:
            table.cellWidget(i, 0).setChecked(False)


def on_press(key):
    # print(key)
    try:
        if key == key.delete:
            Update_Thead.stop_flg = not (Update_Thead.stop_flg)
            print(key)
        elif key == key.page_down:
            Update_Thead.next_flg = True
            print(key)
        elif key == key.home:
            ui.pushButton_start.click()
            print(key)
        elif key == key.end:
            ui.pushButton_stop.click()
            print(key)
    except AttributeError:
        print(key)


class KeyListenerThead(QThread):
    _signal = pyqtSignal(object)

    def __init__(self):
        super(KeyListenerThead, self).__init__()

    def run(self) -> None:
        with pynput.keyboard.Listener(on_press=on_press) as lsn:
            lsn.join()


def flash():
    Flash_Thead.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    # 将import进来的icon.py里的数据转换成临时文件tmp.ico，作为图标
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("tmp.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)
    os.remove("tmp.ico")  # 删掉临时文件

    ui = MyUi()
    ui.setupUi(MainWindow)
    MainWindow.show()

    global speed
    global host_list
    host_list = []
    global host_list1
    host_list1 = []
    global host_list2
    host_list2 = []
    global host_list3
    host_list3 = []

    global d_time
    d_time = []
    global d_time1
    d_time1 = []
    global d_time2
    d_time2 = []
    global d_time3
    d_time3 = []

    global ischecked
    global ischecked1
    global ischecked2
    global ischecked3

    KeyListener_Thead = KeyListenerThead()
    KeyListener_Thead.start()

    Flash_Thead = FlashThead()  #
    Flash_Thead._signal.connect(flashsignal_accept)

    Cmd_Thead = CmdThead()
    Cmd_Thead._signal.connect(signal_accept)

    Update_Thead = UpdateThead()
    Update_Thead.run_flg = False
    Update_Thead._signal.connect(signal_accept)

    ui.pushButton_save.clicked.connect(save_host)
    ui.pushButton_add.clicked.connect(add_host)
    ui.pushButton_start.clicked.connect(start)
    ui.pushButton_stop.clicked.connect(stop)
    ui.pushButton_update.clicked.connect(updatelist)
    ui.pushButton_once.clicked.connect(updateonce)
    ui.pushButton_speed.clicked.connect(modifyGSPD)
    ui.checkBox_selectall.clicked.connect(sel_all)
    ui.radioButton_1.clicked.connect(flash)
    ui.radioButton_2.clicked.connect(flash)
    ui.radioButton_3.clicked.connect(flash)

    deal_yaml()

    sys.exit(app.exec_())
