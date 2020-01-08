#
# @app.route('/score',methods=['POST'])  ##########微信小程序
# def score():
#     res_data=request.json.get('data')
#     print(res_data)
#     if res_data:
#         if list(res_data)[0] in switchChecked :
#             print(list(res_data)[0])
#             pip_num = int(list(res_data)[0][6])
#             print(pip_num)
#             if res_data['switch%sChecked'%(pip_num)] == 0:
#                 pipe_flag[pip_num] = False
#                 print('开关', pip_num, '关闭')
#             elif res_data['switch%sChecked'%(pip_num)] == 1:
#                 pipe_flag[pip_num] = True
#                 print('开关', pip_num, '打开')
#
#
#     # print(res_data)
#     return json.dumps(pipe_flag, ensure_ascii=False)
# encoding:utf-8
# !/usr/bin/env python
#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: flask_websocket_server.py
@time: 2019/2/20 17:24
@describe: 基于flask_socketio实现websocket的服务端
同时借助flask的路由实现任务发布调度与 消息接收
"""
import sys
import os
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit


a=0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

name_space = '/test'  # 命名空间
event_name = 'callback message'  # 消息接收对象
client_query = []


@app.route('/')
def index():
    """加载HTML客户端"""
    return  render_template('index.html')

@app.route('/wechat',methods=['POST'])
def wechat():
    res_data=request.json.get('data')
    print(res_data)
    if res_data:
        return ('ok')
    return 'no'
@app.route('/push')
def push_once():
    """
    客户端发送消息：http://127.0.0.1:5000/push?msg=a
    此方式发布消息见最后一篇代码
    """
    data = request.args.get("msg")
    broadcasted_data = {'data': data}
    print('send msg==>', broadcasted_data)
    print("clicent_query==>", client_query)
    """
    指定客户端方式发送消息，如果需要针对某一客户端发送，则添加room参数： room=client_query[0],
    这里指定第一个连接客户端
    emit(event_name, broadcasted_data, broadcast=False, namespace=name_space, room=client_query[0])
    """

    # 广播方式发送消息
    emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)
    return 'send msg ok!'

def send_command():
    socketio.emit('server_response',
                  {'data': '这是条指令'},
                  namespace='/test2')


# on('消息订阅对象', '命名空间区分')
@socketio.on('message', namespace=name_space)
def test_message(message):
    """ 服务端接收消息 """
    print('recevice message', message)
    # 回传给客户端消息，也可以选择不回传
    emit('callback message', {'data': message}, broadcast=True, namespace=name_space)


@socketio.on('message', namespace='/test2')
def test_message(message):
    """ 服务端接收消息 """
    print('recevice message2', message)
    print(type(message))
    # 回传给客户端消息，也可以选择不回传
    #emit('callback message', {'data': message}, broadcast=True, namespace='/test2')
    send_command()

@socketio.on('my broadcast event', namespace=name_space)
def test_message_2(message):
    print("my response===>", message)
    emit('my response', {'data': message}, broadcast=True)


@socketio.on('connect', namespace=name_space)
def test_connect():
    global a
    # 建立连接 sid:连接对象ID
    client_id = request.sid
    print('1 connected ==> ', client_id)
    a=a+1
    print(a, '个连接')
    client_query.append(client_id)
    emit('connect', '%s connect successful!' % client_id, broadcast=True)

@socketio.on('disconnect', namespace=name_space)
def test_disconnect():
    global a
    # 连接对象关闭 删除对象ID
    client_query.remove(request.sid)
    print('0 Client disconnected==> ', request.sid)
    a = a - 1
    print(a, '个连接')

if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=443, debug=True)
    #socketio.run()函数封装了 Web 服务器的启动，并替换了app.run()标准的 Flask 开发服务器启动