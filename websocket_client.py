#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: test_clicent.py
@time: 2019/2/21 10:31
@describe: 采用 socketio 模块进行消息发布与接收
https://python-socketio.readthedocs.io/en/latest/server.html
"""
import sys
import os,time
import socketio

name_space = '/test2'
sio = socketio.Client()
switchChecked=['switch1Checked', 'switch2Checked',    'switch3Checked', 'switch4Checked',
               'switch5Checked', 'switch6Checked',    'switch7Checked', 'switch8Checked', ]

@sio.on('connect')
def on_connect():
    """创建连接"""
    print('I am connected!')

@sio.on('disconnect')
def on_disconnect():
    """关闭连接"""
    print('I m disconnected!')


@sio.on('relay_control', namespace='/manual_control')
def my_event_handler(res_data):
    # 客户端接收服务端的回调消息  # 接收小程序数据
    # print(res_data)
    if res_data:
        if list(res_data)[0] in switchChecked:  # 判断指令是不是开关控制,控制relay switchChecked=[switch1Checked--switch8Checked]
            pip_num = int(list(res_data)[0][6])
            if res_data['switch%sChecked' % (pip_num)] == 0:
                # GPIO.output(gpio_tuple[pip_num], GPIO.LOW)
                print('开关', pip_num, '关闭')
                # 'server_response'事件名称+ json格式数据 + namespace 命名空间 == 回传 Socket_client
            elif res_data['switch%sChecked' % (pip_num)] == 1:
                # GPIO.output(gpio_tuple[pip_num], GPIO.HIGH)
                print('开关', pip_num, '打开')

    # 接收完消息关闭连接
   # sio.disconnect()
    return "ok!"


# 建立连接对象
if __name__ == '__main__':
    sio.connect('http://localhost:8888')
    while (True):

        time.sleep(1)