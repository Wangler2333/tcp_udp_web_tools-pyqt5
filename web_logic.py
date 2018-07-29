from PyQt5 import QtWidgets
import tcp_udp_web_ui
import stopThreading
import socket
import threading
import re
import sys
import time


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
                time.sleep(0.001)
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
