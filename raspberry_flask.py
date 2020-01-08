# -*- coding: utf-8 -*-
import time,json

import socket,threading
from threading import Thread

from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

# import RPi.GPIO as GPIO


from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit


# import SQL
# import gpio_set
# import sql_datas

app = Flask(__name__)
bootstrap = Bootstrap(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
name_space = '/test'  # 命名空间
event_name = 'callback message'  # 消息接收对象
client_query = []

# SQL.init()
# gpio_set.gpio_model()

pi_socket_ip = ('0.0.0.0', 1996)  # 绑定SOCKET地址
pi_socket_server = None  # 负责监听的socket
pi_socket_pool = []  # 连接池

gpio_tuple = (38, 29, 31, 32, 33, 35, 36, 40)
# Relay1-38  #Relay2-29  #Relay3-31  #Relay4-32
# Relay5-33  #Relay6-35  #Relay6-36  #Relay7-40
relay_status = {'no_1': '', 'no_2': '', 'no_3': '', 'no_4': '', 'no_5': '', 'no_6': '', 'no_7': '', 'no_8': ''}
pipe_flag = [True,True,False,False,False,False,False,False,'']  ## 从0开始排序
switchChecked=['switch1Checked', 'switch2Checked',    'switch3Checked', 'switch4Checked',
               'switch5Checked', 'switch6Checked',    'switch7Checked', 'switch8Checked', ]
start_time_target = 0
end_time_target = 0
irri_pipes_list = []
last_row_data_upload = []


# def get_texts():
#     session = SQL.Session()
#     str_content1 = session.query(SQL.Content).filter(SQL.Content.id == 1).first().text1
#     str_content2 = session.query(SQL.Content).filter(SQL.Content.id == 1).first().text2
#     str_content3 = session.query(SQL.Content).filter(SQL.Content.id == 1).first().text3
#     str_content4 = session.query(SQL.Content).filter(SQL.Content.id == 1).first().text4
#     str_content5 = session.query(SQL.Content).filter(SQL.Content.id == 1).first().text5
#     # contents = [str_content1, str_content2, str_content3, str_content4, str_content5]
#     # print(contents)
#     text_data_list = {'text1': str_content1, 'text2': str_content2, 'text3': str_content3,
#                       'text4': str_content4,
#                       'text5': str_content5}
#     session.commit()
#     session.close()
#     return text_data_list
#
#
# @app.route('/logined_data_update', methods=['GET', 'POST'])
# def logined_data_update():
#     global last_row_data_upload
#     last_row_data_upload = sql_datas.latest_row()  # list
#     # print(contents)
#     last_row_data_upload = {"datas": last_row_data_upload}
#     return jsonify(last_row_data_upload)

@app.route('/logined_jiangwen', methods=['GET', 'POST'])
def logined_jiangwen():
    global last_row_data_upload
    # print(last_row_data_upload)
    if last_row_data_upload:
        current_temp = last_row_data_upload['datas'][0]
        if current_temp >= 35:
            # print('jiangwen')   #换成发短信以及电磁阀控制
            relay_status['no_6'] = 'on'
            GPIO.output(gpio_tuple[5], GPIO.LOW)
            return "ok."
        if current_temp < 35:
            # print('bujiangwen')
            relay_status['no_6'] = 'off'
            GPIO.output(gpio_tuple[5], GPIO.HIGH)
            return "not ok"
    return 'wait for data update！'


@app.route('/logined_jiangwen_manual/', methods=['GET', 'POST'])
def logined_jiangwen_manual():
    time.sleep(0.5)
    relay_status['no_6'] = request.args.get('Relay6')
    GPIO.output(gpio_tuple[5], GPIO.LOW)
    # print ('relay 1 opened')
    # print('手动降温成功') #改成电磁阀控制
    return "手动降温成功"


@app.route('/jiangwen_status/', methods=['GET', 'POST'])
def jiangwen_status():
    time.sleep(0.5)
    if relay_status['no_6'] == 'on':
        return "jiangwenzhong"
    if relay_status['no_6'] == 'off':
        return "tingzhijiangwen"
    return ""


@app.route('/pi_manual?realname=<realname>', methods=['GET', 'POST'])
def pi_manual(realname):
    time_str = time.strftime("%Y-%m-%d %a", time.localtime())
    return render_template('pi_manual.html', time_str=time_str, realname=realname)


@app.route('/pi_buttons_frame/', methods=['GET', 'POST'])
def pi_buttons_frame():
    # form_datas()
    return render_template('pi_buttons_frame.html')


@app.route('/manual_raspberry_control1', methods=['GET'])
def manual_raspberry_control1():
    global relay_status
    relay_status['no_1'] = request.args.get('Relay1')
    # print(relay_status)
    if relay_status['no_1'] == 'on':
        # GPIO.output(gpio_tuple[0], GPIO.LOW)
        print ('relay 1 opened')
    if relay_status['no_1'] == 'off':
        # GPIO.output(gpio_tuple[0], GPIO.HIGH)
        print ('relay 1 closed')
    return ''


@app.route('/manual_raspberry_control2', methods=['GET'])
def manual_raspberry_control2():
    global relay_status
    relay_status['no_2'] = request.args.get('Relay2')
    # print(relay_status)
    if relay_status['no_2'] == 'on':
        # GPIO.output(gpio_tuple[1], GPIO.LOW)
        print ('Relay2 opened')
    if relay_status['no_2'] == 'off':
        print('Relay2 closed')
        # GPIO.output(gpio_tuple[1], GPIO.HIGH)
    return ''


@app.route('/manual_raspberry_control3', methods=['GET'])
def manual_raspberry_control3():
    global relay_status
    relay_status['no_3'] = request.args.get('Relay3')
    # print(relay_status)
    if relay_status['no_3'] == 'on':
        GPIO.output(gpio_tuple[2], GPIO.LOW)
        # print ('Relay3 opened')
    if relay_status['no_3'] == 'off':
        GPIO.output(gpio_tuple[2], GPIO.HIGH)
        # print('Relay3 closed')
    return ''


@app.route('/manual_raspberry_control4', methods=['GET'])
def manual_raspberry_control4():
    global relay_status
    relay_status['no_4'] = request.args.get('Relay4')
    # print(relay_status)
    if relay_status['no_4'] == 'on':
        GPIO.output(gpio_tuple[3], GPIO.LOW)
        # print('rRelay4 opened')
    if relay_status['no_4'] == 'off':
        GPIO.output(gpio_tuple[3], GPIO.HIGH)
        # print('Relay4 closed')
    return ''


@app.route('/manual_raspberry_control5', methods=['GET'])
def manual_raspberry_control5():
    global relay_status
    relay_status['no_5'] = request.args.get('Relay5')
    # print(relay_status)
    if relay_status['no_5'] == 'on':
        GPIO.output(gpio_tuple[4], GPIO.LOW)
        # print('Relay5 opened')
    if relay_status['no_5'] == 'off':
        GPIO.output(gpio_tuple[4], GPIO.HIGH)
        # print('Relay5 closed')
    return ''


@app.route('/manual_raspberry_control6', methods=['GET'])
def manual_raspberry_control6():
    global relay_status
    relay_status['no_6'] = request.args.get('Relay6')
    # print(relay_status)
    if relay_status['no_6'] == 'on':
        GPIO.output(gpio_tuple[5], GPIO.LOW)
        # print('Relay6 opened')
    if relay_status['no_6'] == 'off':
        GPIO.output(gpio_tuple[5], GPIO.HIGH)
        # print('Relay6 closed')
    return ''


@app.route('/manual_raspberry_control7', methods=['GET'])
def manual_raspberry_control7():
    global relay_status
    relay_status['no_7'] = request.args.get('Relay7')
    # print(relay_status)
    if relay_status['no_7'] == 'on':
        GPIO.output(gpio_tuple[6], GPIO.LOW)
        # print('Relay7 opened')
    if relay_status['no_7'] == 'off':
        GPIO.output(gpio_tuple[6], GPIO.HIGH)
        # print('Relay7 closed')
    return ''


@app.route('/manual_raspberry_control8', methods=['GET'])
def manual_raspberry_control8():
    global relay_status
    relay_status['no_8'] = request.args.get('Relay8')
    # print(relay_status)
    if relay_status['no_8'] == 'on':
        GPIO.output(gpio_tuple[7], GPIO.LOW)
        # print('Relay8 opened')
    if relay_status['no_8'] == 'off':
        GPIO.output(gpio_tuple[7], GPIO.HIGH)
        # print('Relay8 closed')
    return ''


@app.route('/manual_raspberry_controlall', methods=['GET'])
def manual_raspberry_controlall():
    global relay_status
    relay_all = request.args.get('Relay_all')
    # print(relay_status)
    if relay_all == 'all':
        relay_status['no_1'] = relay_status['no_2'] = relay_status['no_3'] = relay_status['no_4'] = \
            relay_status['no_5'] = relay_status['no_6'] = relay_status['no_7'] = relay_status['no_8'] = ''
        # print(relay_status)
        GPIO.output(gpio_tuple, GPIO.HIGH)
        # print('Relay All closed')
        return ('Relay All closed')
    return ''


@app.route('/manual_raspberry_control_relay1', methods=['GET', 'POST'])
def manual_raspberry_control_relay1():
    global relay_status
    if relay_status['no_1']:
        # print(relay_status['no_1'])
        return relay_status['no_1']
    return ''


@app.route('/manual_raspberry_control_relay2', methods=['GET', 'POST'])
def manual_raspberry_control_relay2():
    global relay_status
    if relay_status['no_2']:
        # print(relay_status['no_2'])
        return relay_status['no_2']
    return ''


@app.route('/manual_raspberry_control_relay3', methods=['GET', 'POST'])
def manual_raspberry_control_relay3():
    global relay_status
    if relay_status['no_3']:
        # print(relay_status['no_3'])
        return relay_status['no_3']
    return ''


@app.route('/manual_raspberry_control_relay4', methods=['GET', 'POST'])
def manual_raspberry_control_relay4():
    global relay_status
    if relay_status['no_4']:
        # print(relay_status['no_4'])
        return relay_status['no_4']
    return ''


@app.route('/manual_raspberry_control_relay5', methods=['GET', 'POST'])
def manual_raspberry_control_relay5():
    global relay_status
    if relay_status['no_5']:
        # print(relay_status['no_5'])
        return relay_status['no_5']
    return ''


@app.route('/manual_raspberry_control_relay6', methods=['GET', 'POST'])
def manual_raspberry_control_relay6():
    global relay_status
    if relay_status['no_6']:
        # print(relay_status['no_6'])
        return relay_status['no_6']
    return ''


@app.route('/manual_raspberry_control_relay7', methods=['GET', 'POST'])
def manual_raspberry_control_relay7():
    global relay_status
    if relay_status['no_7']:
        # print(relay_status['no_7'])
        return relay_status['no_7']
    return ''


@app.route('/manual_raspberry_control_relay8', methods=['GET', 'POST'])
def manual_raspberry_control_relay8():
    global relay_status
    if relay_status['no_8']:
        # print(relay_status['no_8'])
        return relay_status['no_8']
    return ''


@app.route('/pi_automate?realname=<realname>', methods=['GET', 'POST'])
def pi_automate(realname):
    time_str = time.strftime("%Y-%m-%d %a", time.localtime())
    return render_template('pi_automate.html', realname=realname, time_str=time_str)


@app.route('/pi_buttons_auto_frame/', methods=['GET', 'POST'])
def pi_buttons_auto_frame():
    # form_datas()
    return render_template('pi_buttons_auto_frame.html')


def str_time_to_shijianchuo(time_str):
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


@app.route('/irrigation_start/', methods=['GET', 'POST'])
def irrigation_start():
    global pipe_flag, start_time_target, end_time_target, irri_pipes_list
    irri_pipes_list = []
    rec_data_start_time = request.args.get('time_start')
    rec_data_stop_time = request.args.get('time_stop')

    for i in range(0,8):
        if request.args.get('p{}'.format(i))== 'true':
            pipe_flag[0] = True
    pipe_flag[8] = request.args.get('on_or_off')


    # print(rec_data_start_time)
    # print(rec_data_stop_time)
    # print(pipe_flag)
    # print(pipe_flag[8])
    for i in range(8):
        if pipe_flag[i] == True:
            irri_pipes_list.append(i + 1)
    if 'true' in pipe_flag:
        flag = True
    else:
        flag = False
    # print(flag,'\t',irri_pipes_list)
    if rec_data_start_time and rec_data_stop_time and flag:
        start_time_target_str = rec_data_start_time[0:10] + ' ' + rec_data_start_time[11:] + ':00'
        end_time_target_str = rec_data_stop_time[0:10] + ' ' + rec_data_stop_time[11:] + ':00'
        start_time_target = str_time_to_shijianchuo(start_time_target_str)
        end_time_target = str_time_to_shijianchuo(end_time_target_str)
        # print(start_time_target,'\t',end_time_target)
    return ''


@app.route('/irrigation_duration_control/', methods=['GET', 'POST'])
def irrigation_duration_control():
    global pipe_flag, start_time_target, end_time_target, irri_pipes_list
    current_time = time.time()
    # print(current_time)
    if start_time_target < current_time < end_time_target:
        for pipe_num in irri_pipes_list:
            print("管路%s" % pipe_num, "正在灌溉")
            GPIO.output(gpio_tuple[pipe_num - 1], GPIO.LOW)
        if current_time > end_time_target:
            print('时间到，灌溉停止')
            # GPIO.output(gpio_tuple, GPIO.HIGH)
            pipe_flag = [False, False, False, False, False, False, False, False, '']
            start_time_target = 0
            end_time_target = 0
    if current_time < start_time_target:
        print('等待灌溉启动')
    return ''


@app.route('/automation_raspberry_control_relay1/', methods=['GET', 'POST'])
def automation_raspberry_control_relay1():
    global pipe_flag
    if pipe_flag[0] == 'true':
        # print(pipe_flag[0])
        return pipe_flag[0]
    return 'false'


@app.route('/automation_raspberry_control_relay2/', methods=['GET', 'POST'])
def automation_raspberry_control_relay2():
    global pipe_flag
    if pipe_flag[1] == 'true':
        # print(pipe_flag[1])
        return pipe_flag[1]
    return 'false'


@app.route('/automation_raspberry_control_relay3/', methods=['GET', 'POST'])
def automation_raspberry_control_relay3():
    global pipe_flag
    if pipe_flag[2] == 'true':
        # print(pipe_flag[2])
        return pipe_flag[2]
    return 'false'


@app.route('/automation_raspberry_control_relay4/', methods=['GET', 'POST'])
def automation_raspberry_control_relay4():
    global pipe_flag
    if pipe_flag[3] == 'true':
        # print(pipe_flag[3])
        return pipe_flag[3]
    return 'false'


@app.route('/automation_raspberry_control_relay5/', methods=['GET', 'POST'])
def automation_raspberry_control_relay5():
    global pipe_flag
    if pipe_flag[4] == 'true':
        # print(pipe_flag[4])
        return pipe_flag[4]
    return 'false'


@app.route('/automation_raspberry_control_relay6/', methods=['GET', 'POST'])
def automation_raspberry_control_relay6():
    global pipe_flag
    if pipe_flag[5] == 'true':
        # print(pipe_flag[5])
        return pipe_flag[5]
    return 'false'


@app.route('/automation_raspberry_control_relay7/', methods=['GET', 'POST'])
def automation_raspberry_control_relay7():
    global pipe_flag
    if pipe_flag[6] == 'true':
        # print(pipe_flag[6])
        return pipe_flag[6]
    return 'false'


@app.route('/automation_raspberry_control_relay8/', methods=['GET', 'POST'])
def automation_raspberry_control_relay8():
    global pipe_flag
    if pipe_flag[7] == 'true':
        # print(pipe_flag[7])
        return pipe_flag[7]
    return 'false'


@app.route('/automation_irrigation_status_control/', methods=['GET', 'POST'])
def automation_irrigation_status_control():
    global pipe_flag
    if pipe_flag[8] == 'on':
        # print(pipe_flag[8])
        return pipe_flag[8]
    return 'off'


@app.route('/automation_raspberry_controlall/', methods=['GET', 'POST'])
def automation_raspberry_controlall():
    global pipe_flag, start_time_target, end_time_target
    pipe_flag = [False, False, False, False, False, False, False, False, '']
    start_time_target = 0
    end_time_target = 0
    return ''


@app.route('/pi_images?realname=<realname>', methods=['GET', 'POST'])
def pi_images(realname):
    time_str = time.strftime("%Y-%m-%d %a", time.localtime())
    return render_template('pi_images.html', realname=realname, time_str=time_str)


@app.route('/pi_images_frame/', methods=['GET', 'POST'])
def pi_images_frame():
    # form_datas()
    return render_template('pi_images_frame.html')

#
# @socketio.on('message', namespace='/test2')
# def test_message(message):
#     """ 服务端接收消息 """
#     print('recevice message2', message)
#     print(type(message))
#     # 回传给客户端消息，也可以选择不回传
#     #emit('callback message', {'data': message}, broadcast=True, namespace='/test2')



'''******************微信小程序开关控制部分******************'''
@app.route('/wechat_control',methods=['POST'])
def wechat_control():
    res_data=request.json.get('data')  #接收小程序数据
    print(res_data)
    if res_data:
        if list(res_data)[0] in switchChecked :  #判断指令是不是开关控制,接收小程序数据 switchChecked=[switch1Checked--switch8Checked]
            print(list(res_data)[0])
            pip_num = int(list(res_data)[0][6])
            print(pip_num)
            if res_data['switch%sChecked'%(pip_num)] == 0:
                pipe_flag[pip_num] = False
                print('第',pip_num+1,'个开关关闭')
                socketio.emit('relay_control',{'switch%sChecked'%(pip_num):0},namespace='/manual_control')
                # 'server_response'事件名称+ json格式数据 + namespace 命名空间 == 回传 Socket_client
            elif res_data['switch%sChecked'%(pip_num)] == 1:
                pipe_flag[pip_num] = True
                print('第',pip_num+1,'个开关打开')
                socketio.emit('relay_control', {'switch%sChecked'%(pip_num):1}, namespace='/manual_control')


    # print(res_data)
    return json.dumps(pipe_flag, ensure_ascii=False)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8888, debug=True)
    socketio.run(app, host='0.0.0.0', port=1996, debug=True)
