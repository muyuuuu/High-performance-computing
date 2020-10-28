'''
File: draft.py
Project: 第六次作业(MPI并行矩阵乘法)
===========
File Created: Monday, 26th October 2020 2:14:19 pm
Author: <<LanLing>> (<<lanlingrock@gmail.com>>)
===========
Last Modified: Monday, 26th October 2020 4:27:15 pm
Modified By: <<LanLing>> (<<lanlingrock@gmail.com>>)
===========
Description: MPI for python 练习
Copyright <<projectCreationYear>> - 2020 Your Company, <<XDU>>
ref: https://rabernat.github.io/research_computing/parallel-programming-with-mpi-for-python.html
'''
from mpi4py import MPI
import numpy as np


# # 包含所有进程的默认通信者们
# comm = MPI.COMM_WORLD
# # 获取进程的 id
# comm_rank = comm.Get_rank()

# if comm_rank == 0:
#     print(comm.Get_size())

# print("hello world", end=', ')
# print("my rank is: {}".format(comm_rank))


# # 点到点通信 ----------------------------------------------------------------------------------
# if comm_rank == 0:
#     data = {'a': 7, 'b': 3.14}
#     # dest 指定目标 rank
#     # tag 是消息的 id
#     # 常见的 python 数据对象用小写
#     comm.send(data, dest=1, tag=11)
# elif comm_rank == 1:
#     # source 指定源 rank
#     data = comm.recv(source=0, tag=11)
#     print('On process 1, data is ', data)

# # 发送 numpy ------------
# if comm_rank == 3:
#     numData = 10
#     comm.send(numData, dest=4)

#     data = np.linspace(0.0, 3.14, numData)
#     # 类似缓冲区的对象用大写
#     comm.Send(data, dest=4)

# elif comm_rank == 4:
#     numData = comm.recv(source=3)
#     print('Number of data to receive: ', numData)
#     # 分配出数据区域用于存储接收的数据
#     data = np.empty(numData, dtype='d')
#     comm.Recv(data, source=3)
#     print('data received: ', data)


# 广播通信 ----- bcast ----------------------------------------------------------------
# rank 等于0的root进程初始化了一个变量， variable_to_share ，值为100.这个变量将通过通讯组发送给其他进程。
# from mpi4py import MPI
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# if rank == 0:
#     variable_to_share = 100
# else:
#     variable_to_share = None
# variable_to_share = comm.bcast(variable_to_share, root=0)
# print("process = %d" %rank + " variable shared  = %d " %variable_to_share)


# 广播通信 ----- scatter ----------------------------------------------------------------
# recvbuf 参数表示第i个变量将会通过 comm.scatter 发送给第i个进程：
# from mpi4py import MPI
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# if rank == 0:
#     array_to_share = [1, 2, 3, 4 ,5 ,6 ,7, 8 ,9 ,10]
# else:
#     array_to_share = None
# recvbuf = comm.scatter(array_to_share, root=0)
# print("process = %d" %rank + " recvbuf = %d " %recvbuf)


# 广播通信 ----- gather ----------------------------------------------------------------
# from mpi4py import MPI
# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()
# data = (rank+1)**2
# data = comm.gather(data, root=0)
# if rank == 0:
#     print ("rank = {} ".format(rank) + "...receiving data to other process")
#     for i in range(1, size):
#         data[i] = (i+1)**2
#         value = data[i]
#         print(" process {} receiving {} from process {}".format(rank , value , i))


# import numpy as np
# from mpi4py import MPI
# comm = MPI.COMM_WORLD
# size = comm.size
# rank = comm.rank
# array_size = 4
# recvdata = np.zeros(array_size, dtype=np.int)
# senddata = (rank+1)*np.arange(size,dtype=np.int)
# print("process %s sending %s " % (rank , senddata))
# comm.Reduce(senddata, recvdata, root=0, op=MPI.SUM)
# if rank == 0:
#     print('on task', rank, 'after Reduce:    data = ', recvdata)


#
# from mpi4py import MPI
# import numpy as np

# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()

# # master process
# if rank == 0:
#     data = np.arange(4.)
#     # master process sends data to worker processes by
#     # going through the ranks of all worker processes
#     for i in range(1, size):
#         comm.Send(data, dest=i, tag=i)
#         print('Process {} sent data:'.format(rank), data)

# # worker processes
# else:
#     # initialize the receiving buffer
#     data = np.zeros(4)
#     # receive data from master process
#     comm.Recv(data, source=0, tag=rank)
#     print('Process {} received data:'.format(rank), data)


from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
# 线程数量
nprocs = comm.Get_size()

if rank == 0:
    sendbuf = np.arange(100.0)
    
    # ave 是整除，res 是取余
    ave, res = divmod(sendbuf.size, nprocs)
    # i 比余数小，count = 除数 + 1
    # 否则就是除数
    count = [ave + 1 if i < res else ave for i in range(nprocs)]
    count = np.array(count)

    # 计算子任务的起始索引
    displ = [sum(count[:p]) for p in range(nprocs)]
    displ = np.array(displ)

else:
    sendbuf = None
    # initialize count on worker processes
    count = np.zeros(nprocs, dtype=np.int)
    displ = None

# broadcast count
comm.Bcast(count, root=0)

# 初始化每个进程接收的数据大小
recvbuf = np.zeros(count[rank])

comm.Scatterv([sendbuf, count, displ, MPI.DOUBLE], recvbuf, root=0)


print('After Scatterv, process {} has data:'.format(rank), recvbuf)
