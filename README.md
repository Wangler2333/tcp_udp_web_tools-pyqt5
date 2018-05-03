# tcp_udp_web_tools
配合wangler2333博客创建
博客地址：
http://blog.csdn.net/u010139869/article/details/79505892

逻辑与界面分离的文件：
```
tcp_logic.py
udp_logic.py
web_logic.py
tcp_udp_web_ui.py
```

单文件版本：tcp_udp_web_tools_all_in_one.py

----

运用逻辑与界面分离的思想，使用pyqt5+socket模块编写图形化TCP/UDP/WEB通信工具。
实现效果如图：
![实例1](http://img.blog.csdn.net/20180310105839480?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMDEzOTg2OQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![实例2](http://img.blog.csdn.net/20180310110241424?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMDEzOTg2OQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![实例3](http://img.blog.csdn.net/20180310110314412?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMDEzOTg2OQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

----
## 强制关闭线程的脚本stopThreading.py:
```python
import ctypes
import inspect


def _async_raise(tid, exc_type):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exc_type):
        exc_type = type(exc_type)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# 强制关闭线程的方法
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
```
## 编写界面程序tcp_udp_web_ui.py：
```python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout
import sys


class ToolsUi(QDialog):
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_write_msg = QtCore.pyqtSignal(str)

    def __init__(self, num):
        """
        初始化窗口
        :param num: 计数窗口
        """
        super(ToolsUi, self).__init__()
        self.num = num
        self._translate = QtCore.QCoreApplication.translate

        self.setObjectName("TCP-UDP")
        self.resize(640, 480)
        self.setAcceptDrops(False)
        self.setSizeGripEnabled(False)

        # 定义控件
        self.pushButton_get_ip = QtWidgets.QPushButton()
        self.pushButton_link = QtWidgets.QPushButton()
        self.pushButton_unlink = QtWidgets.QPushButton()
        self.pushButton_clear = QtWidgets.QPushButton()
        self.pushButton_exit = QtWidgets.QPushButton()
        self.pushButton_send = QtWidgets.QPushButton()
        self.pushButton_dir = QtWidgets.QPushButton()
        self.pushButton_else = QtWidgets.QPushButton()
        self.label_port = QtWidgets.QLabel()
        self.label_ip = QtWidgets.QLabel()
        self.label_rev = QtWidgets.QLabel()
        self.label_send = QtWidgets.QLabel()
        self.label_sendto = QtWidgets.QLabel()
        self.label_dir = QtWidgets.QLabel()
        self.label_written = QtWidgets.QLabel()
        self.lineEdit_port = QtWidgets.QLineEdit()
        self.lineEdit_ip_send = QtWidgets.QLineEdit()
        self.lineEdit_ip_local = QtWidgets.QLineEdit()
        self.textEdit_send = QtWidgets.QTextEdit()
        self.textBrowser_recv = QtWidgets.QTextBrowser()
        self.comboBox_tcp = QtWidgets.QComboBox()

        # 定义布局
        self.h_box_1 = QHBoxLayout()
        self.h_box_2 = QHBoxLayout()
        self.h_box_3 = QHBoxLayout()
        self.h_box_4 = QHBoxLayout()
        self.h_box_recv = QHBoxLayout()
        self.h_box_exit = QHBoxLayout()
        self.h_box_all = QHBoxLayout()
        self.v_box_set = QVBoxLayout()
        self.v_box_send = QVBoxLayout()
        self.v_box_web = QVBoxLayout()
        self.v_box_exit = QVBoxLayout()
        self.v_box_right = QVBoxLayout()
        self.v_box_left = QVBoxLayout()

        # 向选择功能的下拉菜单添加选项
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")
        self.comboBox_tcp.addItem("")

        # 设置字体
        font = QtGui.QFont()
        font.setFamily("Yuppy TC")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_rev.setFont(font)
        self.label_send.setFont(font)

        # 设置控件的初始属性
        self.label_dir.hide()
        self.label_sendto.hide()
        self.pushButton_dir.hide()
        self.lineEdit_ip_send.hide()
        self.label_dir.setWordWrap(True)  # 让label自动换行
        self.pushButton_unlink.setEnabled(False)
        self.textBrowser_recv.insertPlainText("这是窗口-%s\n" % self.num)

        # 调用布局方法和控件显示文字的方法
        self.layout_ui()
        self.ui_translate()
        self.connect()

    def layout_ui(self):
        """
        设置控件的布局
        :return:
        """
        # 左侧布局添加
        self.h_box_1.addWidget(self.label_ip)
        self.h_box_1.addWidget(self.lineEdit_ip_local)
        self.h_box_1.addWidget(self.pushButton_get_ip)
        self.h_box_2.addWidget(self.label_port)
        self.h_box_2.addWidget(self.lineEdit_port)
        self.h_box_2.addWidget(self.pushButton_else)
        self.h_box_3.addWidget(self.label_sendto)
        self.h_box_3.addWidget(self.lineEdit_ip_send)
        self.h_box_4.addWidget(self.comboBox_tcp)
        self.h_box_4.addWidget(self.pushButton_link)
        self.h_box_4.addWidget(self.pushButton_unlink)
        self.v_box_set.addLayout(self.h_box_1)
        self.v_box_set.addLayout(self.h_box_2)
        self.v_box_set.addLayout(self.h_box_3)
        self.v_box_set.addLayout(self.h_box_4)
        self.v_box_web.addWidget(self.label_dir)
        self.v_box_web.addWidget(self.pushButton_dir)
        self.v_box_send.addWidget(self.label_send)
        self.v_box_send.addWidget(self.textEdit_send)
        self.v_box_send.addLayout(self.v_box_web)
        self.v_box_exit.addWidget(self.pushButton_send)
        self.v_box_exit.addWidget(self.pushButton_exit)
        self.h_box_exit.addWidget(self.label_written)
        self.h_box_exit.addLayout(self.v_box_exit)
        self.v_box_left.addLayout(self.v_box_set)
        self.v_box_left.addLayout(self.v_box_send)
        self.v_box_left.addLayout(self.h_box_exit)

        # 右侧布局添加
        self.h_box_recv.addWidget(self.label_rev)
        self.h_box_recv.addWidget(self.pushButton_clear)
        self.v_box_right.addLayout(self.h_box_recv)
        self.v_box_right.addWidget(self.textBrowser_recv)

        # 将左右布局添加到窗体布局
        self.h_box_all.addLayout(self.v_box_left)
        self.h_box_all.addLayout(self.v_box_right)

        # 设置窗体布局到窗体
        self.setLayout(self.h_box_all)

    def ui_translate(self):
        """
        控件默认显示文字的设置
        :param : QDialog类创建的对象
        :return: None
        """
        # 设置各个控件显示的文字
        # 也可使用控件的setText()方法设置文字
        self.setWindowTitle(self._translate("TCP-UDP", "TCP/UDP网络测试工具-窗口%s" % self.num))
        self.comboBox_tcp.setItemText(0, self._translate("TCP-UDP", "TCP服务端"))
        self.comboBox_tcp.setItemText(1, self._translate("TCP-UDP", "TCP客户端"))
        self.comboBox_tcp.setItemText(2, self._translate("TCP-UDP", "UDP服务端"))
        self.comboBox_tcp.setItemText(3, self._translate("TCP-UDP", "UDP客户端"))
        self.comboBox_tcp.setItemText(4, self._translate("TCP-UDP", "WEB服务端"))
        self.pushButton_link.setText(self._translate("TCP-UDP", "连接网络"))
        self.pushButton_unlink.setText(self._translate("TCP-UDP", "断开网络"))
        self.pushButton_get_ip.setText(self._translate("TCP-UDP", "重新获取IP"))
        self.pushButton_clear.setText(self._translate("TCP-UDP", "清除消息"))
        self.pushButton_send.setText(self._translate("TCP-UDP", "发送"))
        self.pushButton_exit.setText(self._translate("TCP-UDP", "退出系统"))
        self.pushButton_dir.setText(self._translate("TCP-UDP", "选择路径"))
        self.pushButton_else.setText(self._translate("TCP-UDP", "窗口多开another"))
        self.label_ip.setText(self._translate("TCP-UDP", "本机IP:"))
        self.label_port.setText(self._translate("TCP-UDP", "端口号:"))
        self.label_sendto.setText(self._translate("TCP-UDP", "目标IP:"))
        self.label_rev.setText(self._translate("TCP-UDP", "接收区域"))
        self.label_send.setText(self._translate("TCP-UDP", "发送区域"))
        self.label_dir.setText(self._translate("TCP-UDP", "请选择index.html所在的文件夹"))
        self.label_written.setText(self._translate("TCP-UDP", "Written by Wangler2333"))

    def connect(self):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        self.signal_write_msg.connect(self.write_msg)
        self.comboBox_tcp.currentIndexChanged.connect(self.combobox_change)

    def combobox_change(self):
        # 此函数用于选择不同功能时界面会作出相应变化
        """
        combobox控件内容改变时触发的槽
        :return: None
        """
        self.close_all()
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 2:
            self.label_sendto.hide()
            self.label_dir.hide()
            self.pushButton_dir.hide()
            self.pushButton_send.show()
            self.lineEdit_ip_send.hide()
            self.textEdit_send.show()
            self.label_port.setText(self._translate("TCP-UDP", "端口号:"))

        if self.comboBox_tcp.currentIndex() == 1 or self.comboBox_tcp.currentIndex() == 3:
            self.label_sendto.show()
            self.label_dir.hide()
            self.pushButton_dir.hide()
            self.pushButton_send.show()
            self.lineEdit_ip_send.show()
            self.textEdit_send.show()
            self.label_port.setText(self._translate("TCP-UDP", "目标端口:"))

        if self.comboBox_tcp.currentIndex() == 4:
            self.label_sendto.hide()
            self.label_dir.show()
            self.pushButton_dir.show()
            self.pushButton_send.hide()
            self.lineEdit_ip_send.hide()
            self.textEdit_send.hide()
            self.label_port.setText(self._translate("TCP-UDP", "端口号:"))

    def write_msg(self, msg):
        # signal_write_msg信号会触发这个函数
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的
        :return: None
        """
        self.textBrowser_recv.insertPlainText(msg)
        # 滚动条移动到结尾
        self.textBrowser_recv.moveCursor(QtGui.QTextCursor.End)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        self.close_all()

    def close_all(self):
        pass


if __name__ == '__main__':
    """
    显示界面
    """
    app = QApplication(sys.argv)
    ui = ToolsUi(1)
    ui.show()
    sys.exit(app.exec_())

```

## 编写TCP服务端及客户端逻辑tcp_logic.py：
```python
from PyQt5 import QtWidgets
from tcp_udp_web_tools import tcp_udp_web_ui
import socket
import threading
import sys
import stopThreading


class TcpLogic(tcp_udp_web_ui.ToolsUi):
    def __init__(self, num):
        super(TcpLogic, self).__init__(num)
        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()

        self.link = False  # 用于标记是否开启了连接

    def tcp_server_start(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            port = int(self.lineEdit_port.text())
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg.emit(msg)
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            msg = 'TCP服务端正在监听端口:%s\n' % str(port)
            self.signal_write_msg.emit(msg)

    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                msg = 'TCP服务端已连接IP:%s端口:%s\n' % client_address
                self.signal_write_msg.emit(msg)
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0], address[1], msg)
                        self.signal_write_msg.emit(msg)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def tcp_client_start(self):
        """
        功能函数，TCP客户端连接其他服务端的方法
        :return:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            address = (str(self.lineEdit_ip_send.text()), int(self.lineEdit_port.text()))
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                msg = '正在连接目标服务器\n'
                self.signal_write_msg.emit(msg)
                self.tcp_socket.connect(address)
            except Exception as ret:
                msg = '无法连接目标服务器\n'
                self.signal_write_msg.emit(msg)
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency, args=(address,))
                self.client_th.start()
                msg = 'TCP客户端已连接IP:%s端口:%s\n' % address
                self.signal_write_msg.emit(msg)

    def tcp_client_concurrency(self, address):
        """
        功能函数，用于TCP客户端创建子线程的方法，阻塞式接收
        :return:
        """
        while True:
            recv_msg = self.tcp_socket.recv(1024)
            if recv_msg:
                msg = recv_msg.decode('utf-8')
                msg = '来自IP:{}端口:{}:\n{}\n'.format(address[0], address[1], msg)
                self.signal_write_msg.emit(msg)
            else:
                self.tcp_socket.close()
                self.reset()
                msg = '从服务器断开连接\n'
                self.signal_write_msg.emit(msg)
                break

    def tcp_send(self):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                if self.comboBox_tcp.currentIndex() == 0:
                    # 向所有连接的客户端发送消息
                    for client, address in self.client_socket_list:
                        client.send(send_msg)
                    msg = 'TCP服务端已发送\n'
                    self.signal_write_msg.emit(msg)
                if self.comboBox_tcp.currentIndex() == 1:
                    self.tcp_socket.send(send_msg)
                    msg = 'TCP客户端已发送\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

    def tcp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox_tcp.currentIndex() == 0:
            try:
                for client, address in self.client_socket_list:
                    client.close()
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 1:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TcpLogic(1)
    ui.show()
    sys.exit(app.exec_())

```
## 编写UDP服务端及客户端逻辑udp_logic.py：
```python
from PyQt5 import QtWidgets
from tcp_udp_web_tools import tcp_udp_web_ui
import stopThreading
import socket
import threading
import sys


class UdpLogic(tcp_udp_web_ui.ToolsUi):
    def __init__(self, num):
        super(UdpLogic, self).__init__(num)
        self.udp_socket = None
        self.address = None
        self.sever_th = None

    def udp_server_start(self):
        """
        开启UDP服务端方法
        :return:
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            port = int(self.lineEdit_port.text())
            address = ('', port)
            self.udp_socket.bind(address)
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg.emit(msg)
        else:
            self.sever_th = threading.Thread(target=self.udp_server_concurrency)
            self.sever_th.start()
            msg = 'UDP服务端正在监听端口:{}\n'.format(port)
            self.signal_write_msg.emit(msg)

    def udp_server_concurrency(self):
        """
        用于创建一个线程持续监听UDP通信
        :return:
        """
        while True:
            recv_msg, recv_addr = self.udp_socket.recvfrom(1024)
            msg = recv_msg.decode('utf-8')
            msg = '来自IP:{}端口:{}:\n{}\n'.format(recv_addr[0], recv_addr[1], msg)
            self.signal_write_msg.emit(msg)

    def udp_client_start(self):
        """
        确认UDP客户端的ip及地址
        :return:
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.address = (str(self.lineEdit_ip_send.text()), int(self.lineEdit_port.text()))
        except Exception as ret:
            msg = '请检查目标IP，目标端口\n'
            self.signal_write_msg.emit(msg)
        else:
            msg = 'UDP客户端已启动\n'
            self.signal_write_msg.emit(msg)

    def udp_send(self):
        """
        功能函数，用于UDP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = (str(self.textEdit_send.toPlainText())).encode('utf-8')
                if self.comboBox_tcp.currentIndex() == 2:
                    msg = 'UDP服务端无法发送，请切换为UDP客户端\n'
                    self.signal_write_msg.emit(msg)
                if self.comboBox_tcp.currentIndex() == 3:
                    self.udp_socket.sendto(send_msg, self.address)
                    msg = 'UDP客户端已发送\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

    def udp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox_tcp.currentIndex() == 2:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        if self.comboBox_tcp.currentIndex() == 3:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UdpLogic(1)
    ui.show()
    sys.exit(app.exec_())

```

## 编写WEB服务端逻辑web_logic.py：
```python
from PyQt5 import QtWidgets
from tcp_udp_web_tools import tcp_udp_web_ui
import stopThreading
import socket
import threading
import re
import sys


class WebLogic(tcp_udp_web_ui.ToolsUi):
    def __init__(self, num):
        super(WebLogic, self).__init__(num)
        self.tcp_socket = None
        self.sever_th = None
        self.dir = None
        self.client_socket_list = list()

    def web_server_start(self):
        """
        功能函数，WEB服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            port = int(self.lineEdit_port.text())
            self.tcp_socket.bind(('', port))
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg.emit(msg)
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.web_server_concurrency)
            self.sever_th.start()
            msg = 'WEB服务端正在监听端口:%s\n' % str(port)
            self.signal_write_msg.emit(msg)

    def web_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表
                self.client_socket_list.append((client_socket, client_address))
                msg = 'WEB服务端已连接浏览器，IP:%s端口:%s\n' % client_address
                self.signal_write_msg.emit(msg)
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = recv_msg.decode('utf-8')
                        msg_lines = msg.splitlines()
                        msg_dir = re.match(r"[^/]+(/[^ ]*)", msg_lines[0])
                        msg_dir = msg_dir.group(1)
                        msg = '来自IP:{}端口:{}:\n请求路径:{}\n'.format(address[0], address[1], msg_dir)
                        self.signal_write_msg.emit(msg)
                        self.web_send(client, msg_dir)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))

    def web_get_dir(self):
        """
        获取用户选择的路径
        保存到self.dir中，并显示出来
        :return: 
        """
        self.dir = QtWidgets.QFileDialog.getExistingDirectory(self, "获取文件夹路径", './')
        if self.dir:
            self.label_dir.setText(self._translate("TCP-UDP", "%s" % self.dir))

    def web_send_msg(self, msg_dir):
        """
        构造浏览器请求后返回的数据
        :param msg_dir: 浏览器请求的路径
        :return: header头文件，body数据
        """
        # 指定主页路径
        if str(msg_dir) == '/':
            msg_dir = '/index.html'
            dir = str(self.dir) + str(msg_dir)
        else:
            dir = str(self.dir) + str(msg_dir)
        
        # 根据返回文件的类型，制作相应的Content-Type数据
        file_header = self.web_file_header(msg_dir)
        
        # 打开相应的文件，并读取
        try:
            with open(dir, 'rb') as f:
                file = f.read()
        except Exception as ret:
            # 如果打不开文件
            file = '你要的东西不见了'.encode('utf-8')
            response_header = ('HTTP/1.1 404 NOT FOUND\r\n' +
                               'Connection: Keep-Alive\r\n' +
                               'Content-Length: %d\r\n' % len(file) +
                               file_header +
                               '\r\n')
        else:
            # 如果打开了文件
            response_header = ('HTTP/1.1 200 OK\r\n' +
                               'Connection: Keep-Alive\r\n' +
                               'Content-Length: %d\r\n' % len(file) +
                               file_header +
                               '\r\n')
        response_body = file

        return response_header.encode('utf-8'), response_body

    @staticmethod
    def web_file_header(msg_dir):
        """
        根据返回文件的类型，制作相应的Content-Type数据
        :param msg_dir: 历览器请求的路径
        :return: Content-Type数据
        """
        try:
            file_type = re.match(r'[^.]+\.(.*)$', msg_dir)
            file_type = file_type.group(1)
            if file_type == 'png':
                file_header = 'Content-Type: image/%s; charset=utf-8\r\n' % file_type
            elif file_type == 'css' or file_type == 'html':
                file_header = 'Content-Type: text/%s; charset=utf-8\r\n' % file_type
            else:
                file_header = 'Content-Type: text/html; charset=utf-8\r\n'
        except Exception as ret:
            file_header = 'Content-Type: text/html; charset=utf-8\r\n'
            return file_header
        else:
            return file_header

    def web_send(self, client, msg_dir):
        """
        WEB服务器发送消息的方法
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                # 通过web_send_msg方法构造头文件及数据
                header, body = self.web_send_msg(msg_dir)
                client.send(header)
                client.send(body)
                msg = 'WEB服务端已回复\n'
                self.signal_write_msg.emit(msg)
            except Exception as ret:
                print(ret)
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

    def web_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            for client, address in self.client_socket_list:
                client.close()
            self.tcp_socket.close()
            if self.link is True:
                msg = '已断开网络\n'
                self.signal_write_msg.emit(msg)
        except Exception as ret:
            pass
        try:
            stopThreading.stop_thread(self.sever_th)
        except Exception:
            pass
        try:
            stopThreading.stop_thread(self.client_th)
        except Exception:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = WebLogic(1)
    ui.show()
    sys.exit(app.exec_())

```

## 编写main.py将逻辑与界面组合起来：
```python
from PyQt5 import QtWidgets
from tcp_udp_web_tools import tcp_logic, udp_logic, web_logic
import socket
import sys


class MainWindow(tcp_logic.TcpLogic, udp_logic.UdpLogic, web_logic.WebLogic):
    def __init__(self, num):
        super(MainWindow, self).__init__(num)
        self.client_socket_list = list()
        self.another = None
        self.link = False

        # 打开软件时默认获取本机ip
        self.click_get_ip()

    def connect(self, ):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        # 如需传递参数可以修改为connect(lambda: self.click(参数))
        super(MainWindow, self).connect()
        self.pushButton_link.clicked.connect(self.click_link)
        self.pushButton_unlink.clicked.connect(self.click_unlink)
        self.pushButton_get_ip.clicked.connect(self.click_get_ip)
        self.pushButton_clear.clicked.connect(self.click_clear)
        self.pushButton_send.clicked.connect(self.send)
        self.pushButton_dir.clicked.connect(self.click_dir)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_else.clicked.connect(self.another_window)

    def click_link(self):
        """
        pushbutton_link控件点击触发的槽
        :return: None
        """
        # 连接时根据用户选择的功能调用函数
        if self.comboBox_tcp.currentIndex() == 0:
            self.tcp_server_start()
        if self.comboBox_tcp.currentIndex() == 1:
            self.tcp_client_start()
        if self.comboBox_tcp.currentIndex() == 2:
            self.udp_server_start()
        if self.comboBox_tcp.currentIndex() == 3:
            self.udp_client_start()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_server_start()
        self.link = True
        self.pushButton_unlink.setEnabled(True)
        self.pushButton_link.setEnabled(False)

    def click_unlink(self):
        """
        pushbutton_unlink控件点击触发的槽
        :return: None
        """
        # 关闭连接
        self.close_all()
        self.link = False
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def click_get_ip(self):
        """
        pushbutton_get_ip控件点击触发的槽
        :return: None
        """
        # 获取本机ip
        self.lineEdit_ip_local.clear()
        my_addr = socket.gethostbyname(socket.gethostname())
        self.lineEdit_ip_local.setText(str(my_addr))

    def send(self):
        """
        pushbutton_send控件点击触发的槽
        :return: 
        """
        # 连接时根据用户选择的功能调用函数
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.tcp_send()
        if self.comboBox_tcp.currentIndex() == 2 or self.comboBox_tcp.currentIndex() == 3:
            self.udp_send()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_send()

    def click_clear(self):
        """
        pushbutton_clear控件点击触发的槽
        :return: None
        """
        # 清空接收区屏幕
        self.textBrowser_recv.clear()

    def click_dir(self):
        # WEB服务端功能中选择路径
        self.web_get_dir()

    def close_all(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        # 连接时根据用户选择的功能调用函数
        if self.comboBox_tcp.currentIndex() == 0 or self.comboBox_tcp.currentIndex() == 1:
            self.tcp_close()
        if self.comboBox_tcp.currentIndex() == 2 or self.comboBox_tcp.currentIndex() == 3:
            self.udp_close()
        if self.comboBox_tcp.currentIndex() == 4:
            self.web_close()
        self.reset()

    def reset(self):
        """
        功能函数，将按钮重置为初始状态
        :return:None
        """
        self.link = False
        self.client_socket_list = list()
        self.pushButton_unlink.setEnabled(False)
        self.pushButton_link.setEnabled(True)

    def another_window(self):
        """
        开启一个新的窗口的方法
        :return:
        """
        # 弹出一个消息框，提示开启了一个新的窗口
        QtWidgets.QMessageBox.warning(self,
                                      'TCP/UDP网络测试助手',
                                      "已经开启了新的TCP/UDP网络测试助手！",
                                      QtWidgets.QMessageBox.Yes)
        # 计数，开启了几个窗口
        self.num = self.num + 1
        # 开启新的窗口
        self.another = MainWindow(self.num)
        self.another.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow(1)
    ui.show()
    sys.exit(app.exec_())

```

## 继承关系
```flow
st=>start: tcp_udp_web_ui.py
e=>end: main.py
op=>operation: tcp_logic.py//udp_logic.py//web_logic.py
cond=>condition: 继承

st->op->e
```

## 相关代码下载
[下载链接](https://github.com/Wangler2333/tcp_udp_web_tools-pyqt5)
