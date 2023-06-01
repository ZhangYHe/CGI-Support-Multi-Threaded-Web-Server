import socket
from CGI_Worker import task_queue, working_thread, worker, sema
import threading
import time

# 最大连接数
max_connection = 5
port = 8888

# 主线程
# 创建socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_name = socket.gethostbyname(host_name)
address = ("0.0.0.0", port)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)
server_socket.settimeout(60)
server_socket.listen(2)

print("-> Server : Info ",end="")
print(host_name + ':' + str(port))

class thread_pool(threading.Thread):
    def __init__(self, log_name):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()
        self.log_name = log_name

    def run(self):
        # 创建工作线程
        for i in range(max_connection):
            worker(log_name)
        while True:
            for i in range(10):
                # print(len(working_thread), task_queue.empty())
                # 同时打开的连接总数超过maxConnections，服务器关闭最老的连接
                if (len(working_thread) == max_connection and max_connection != 0 and (not task_queue.empty())):
                    print("-> Server : shutdown a working_thread")
                    working_thread[0].restart()
                # time.sleep(0.1)

            # 获得线程信号量，最多阻塞1秒
            sema.acquire(timeout=1)

            working_thread_cnt = len(working_thread)
            print("-> Server : now working thread: " + str(working_thread_cnt) +
                  " ; free thread: " +
                  str(max_connection - working_thread_cnt) +
                  " ; now waiting request: " + str(task_queue.qsize()))


# 创建日志文件
begin_time = time.localtime()
log_name = "log/" + str(begin_time.tm_year) + "-" + str(
    begin_time.tm_mon) + "-" + str(begin_time.tm_mday) + "-" + str(
    begin_time.tm_hour) + "-" + str(begin_time.tm_min) + "-" + str(
    begin_time.tm_sec) + ".txt"

#print(log_name)
thread_pool(log_name)

while True:
    try:
        client, addr = server_socket.accept()
        print("-> Server : recv: ", client.getpeername(), client.getsockname())
        task_queue.put(client)
        # ！！！！ qsize不是阻塞的 当多个请求同时到达qsize不是当前的值
        # if (working_thread.qsize() == max_connection):
        #     working_thread.get().restart()

    except socket.timeout:
        print("-> Server : main server timeout")
