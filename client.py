import socket
import json

# 1.创建socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 链接服务器
server_addr = ("192.168.4.4", 9760)
tcp_socket.connect(server_addr)

# 3. 发送数据
send_data1 = {
    "dsID": "HCRemoteMonitor",
    "cmdType": "command",
    # 800，6，0，左右，前后， 上下，摄像头左右旋转，摄像头上下，镜头旋转
    "cmdData": ["rewriteDataList", "800", "6", "0", "30000", "-30000", "30000", "-30000", "20000", "-30000"]
}
send_data = {"startButton": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["startButton"]},  # 启动按钮
             "stopButton": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["stopButton"]},  # 停止按钮
             "actionStop": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionStop"]},  # 立即停止
             "actionPause": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionPause"]},  # 暂停当前动作
             "actionSingleCycle": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionSingleCycle"]},
             # 进入单循环
             "clearAlarmRunNext": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["clearAlarmRunNext"]},
             # 清除报警后运行下一条指令
             "clearAlarmContinue": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["clearAlarmContinue"]},
             # 清除报警后继续运行条指令
             "modifyGSPD": {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["modifyGSPD", "10"]},
             # 全局速度修改:("d1":速度)
             "rewriteData": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                             "cmdData": ["rewriteData", "800", "6", "0"]},
             # 数据修改:("d1":addrs,"d2":value,"d3":savable)
             "rewriteDataList": {"dsID": "HCRemoteMonitor", "cmdType": "command",
                                 "cmdData": ["rewriteDataList", "800", "6", "0", "0", "0", "0", "0", "-60000", "0"]},
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

print(send_data["stopButton"])

tcp_socket.send(json.dumps(send_data1).encode("gbk"))
# tcp_socket.send(json.dumps(send_data["startButton"]).encode("gbk"))
# tcp_socket.send(json.dumps(send_data["stopButton"]).encode("gbk"))
# tcp_socket.send(json.dumps(send_data["modifyGSPD"]).encode("gbk"))

# 接收响应
response = tcp_socket.recv(4096)

# 打印响应
print(response.decode('utf-8'))

# 4. 关闭套接字
tcp_socket.close()
