#!/usr/bin/python
#-*-coding:utf-8-*-

import zmq
import sys

#https://www.cnblogs.com/binchen-china/p/5643531.html

#1.Request-Reply模式：
# 客户端在请求后，服务端必须回响应
def client_request():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")

    for i in range(10):
        name = "usernmae-" + str(i)
        socket.send(name)
        response = socket.recv();
        print response

#2.Publish-Subscribe模式:
# 广播所有client，没有队列缓存，断开连接数据将永远丢失。client可以进行数据过滤。
def client_subcriber():
    context = zmq.Context()  
    socket = context.socket(zmq.SUB)  
    socket.connect("tcp://127.0.0.1:5000")  
    socket.setsockopt(zmq.SUBSCRIBE,'') 
    while True:  
        print  socket.recv()

# 3.Parallel Pipeline模式：
# 由三部分组成，push进行数据推送，work进行数据缓存，pull进行数据竞争获取处理。区别于Publish-Subscribe存在一个数据缓存和处理负载。
# 当连接被断开，数据不会丢失，重连后数据继续发送到对端。
def client_push():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind('tcp://127.0.0.1:5557')
    while True:
        data = raw_input('input your data:')
        socket.send(data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        m = sys.argv[1]
        if m == '1':
            client_request()
        elif m == '2':
            client_subcriber()
        elif m == '3':
            client_push()




            