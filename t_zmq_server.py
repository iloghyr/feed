#!/usr/bin/python
# _*_ coding=utf-8 _*_

import time
import zmq
import sys



#1.Request-Reply模式：
# 客户端在请求后，服务端必须回响应
def server_reply():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://0.0.0.0:5555")

    while True:
        message = socket.recv()
        print message
        #time.sleep(1)
        socket.send("server response: hello " + message)

#2.Publish-Subscribe模式:
# 广播所有client，没有队列缓存，断开连接数据将永远丢失。client可以进行数据过滤。
def server_publish():
    context = zmq.Context()  
    socket = context.socket(zmq.PUB)  
    socket.bind("tcp://127.0.0.1:5000")  
    while True:  
        msg = raw_input('input your data:') 
        socket.send(msg)

# 3.Parallel Pipeline模式：
# 由三部分组成，push进行数据推送，work进行数据缓存，pull进行数据竞争获取处理。区别于Publish-Subscribe存在一个数据缓存和处理负载。
# 当连接被断开，数据不会丢失，重连后数据继续发送到对端。
def server_pull():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind('tcp://127.0.0.1:5558')

    while True:
        data = socket.recv()
        print data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            server_reply()
        if sys.argv[1] == '2':
            server_publish()
        if sys.argv[1] == '3':
            server_pull()
