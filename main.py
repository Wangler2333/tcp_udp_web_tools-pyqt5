from PyQt5 import QtWidgets
import tcp_logic, udp_logic, web_logic
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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()[0]
            self.lineEdit_ip_local.setText(str(my_addr))
        except Exception as ret:
            # 若无法连接互联网使用，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
                self.lineEdit_ip_local.setText(str(my_addr))
            except Exception as ret_e:
                self.signal_write_msg.emit("无法获取ip，请连接网络！\n")
        finally:
            s.close()

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
