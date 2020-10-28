from mpi4py import MPI
import numpy as np
import time


class DATA():
    '''
    功能表述：生成两个随机的矩阵，取值范围是 [0, 1] 之间的小数
    输入参数：
        ROW1：int，第一个矩阵的行
        COL1：int，第一个矩阵的列
        COL2：int，第二个矩阵的列
    输出参数：
        a：np.array，第一个矩阵
        b：np.array，第二个矩阵
    '''
    def __init__(self, ROW1, COL1, COL2):
        self._row1 = ROW1
        self._col1 = COL1
        self._col2 = COL2

    # 调用私有函数
    def gene_data(self):
        seed = 100
        return self._gene_data(seed)
    
    # 生成矩阵
    def _gene_data(self, seed):
        np.random.seed(seed)
        a = np.random.rand(self._row1, self._col1)
        b = np.random.rand(self._col1, self._col2)
        return a, b


class MatrixMultiply():
    '''
    功能描述：实现矩阵的串行乘法和并行乘法，并对结果进行检验
    输入参数：
        m1：np.array，第一个矩阵
        m2：np.array，第二个矩阵
    输出参数：

    '''
    def __init__(self, m1, m2):
        self._m1 = m1
        self._m2 = m2
        # 判断矩阵规模是大还是小
        self._judge = 200
        # 记录矩阵的大小
        self._r1 = self._m1.shape[0]
        self._c1 = self._m1.shape[1]
        self._c2 = self._m2.shape[1]

    # 实现串行乘法
    def single_multiply(self):
        self._single_multiply()

    def _single_multiply(self):
        # 用于填充串行乘法的结果
        self._single_result = np.zeros((self._m1.shape[0], self._m2.shape[1]))
        temp = 0
        start = time.time()
        # np.dot(self._m1, self._m2)
        for i in range(self._m1.shape[0]):
            for k in range(self._m2.shape[1]):
                for j in range(self._m1.shape[1]):
                    temp = self._m1[i,j] * self._m2[j,k]
                self._single_result[i,k] = temp
        end = time.time()
        # 记录串行乘法执行的时间
        self._single_time = end - start
        print('single ', self._single_time)

    # 实现并行乘法
    def multiprocesses_multi(self):
        self._multiprocesses()

    def _multiprocesses(self):
        #  其中一个矩阵的行列向量都很小 按照小矩阵进行划分
        if (self._m1.shape[0] < self._judge and self._m1.shape[1] < self._judge) or \
            (self._m2.shape[0] < self._judge and self._m2.shape[1] < self._judge):
            self._multi_times()
        #  两个矩阵都很小，不考虑并行加速
        elif (self._m1.shape[0] < self._judge and self._m1.shape[1] < self._judge) and \
            (self._m2.shape[0] < self._judge and self._m2.shape[1] < self._judge):
            self._single_multiply()
        # 两个矩阵规模都很大，规模相当
        # 按照进程的数量对任务进行划分
        else:
            self._multi_times()
    
    # 按照进程数量划分块
    def _multi_times(self):
        since = time.time()
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        # 线程数量
        nprocs = comm.Get_size()
        if rank == 0:
            sendbuf1 = self._m1.flatten()

            # ave 是整除，res 是取余
            ave1, res1 = divmod(self._r1, nprocs)
            # i 比余数小，count = 除数 + 1
            # 否则就是除数
            count1 = [(ave1 + 1)*self._c1 if i < res1 else ave1 * self._c1 for i in range(nprocs)]
            count1 = np.array(count1)

            # 计算子任务的起始索引
            displ1 = [sum(count1[:p]) for p in range(nprocs)]
            displ1 = np.array(displ1)

            sendbuf2 = self._m2.T.flatten('F')

            # ave 是整除，res 是取余
            ave2, res2 = divmod(self._c2, nprocs)
            # i 比余数小，count = 除数 + 1
            # 否则就是除数
            count2 = [(ave2 + 1)*self._c1 if i < res2 else ave2 * self._c1 for i in range(nprocs)]
            count2 = np.array(count2)

            # 计算子任务的起始索引
            displ2 = [sum(count2[:p]) for p in range(nprocs)]
            displ2 = np.array(displ2)

        else:
            sendbuf1 = None
            # initialize count on worker processes
            count1 = np.zeros(nprocs, dtype=np.int)
            # print(count)
            displ1 = None

            sendbuf2 = None
            count2 = np.zeros(nprocs, dtype=np.int)
            displ2 = None

        # broadcast count
        comm.Bcast(count1, root=0)
        # 初始化每个进程接收的数据大小
        recvbuf1 = np.zeros(count1[rank])
        comm.Scatterv([sendbuf1, count1, displ1, MPI.DOUBLE], recvbuf1, root=0)

        comm.Bcast(count2, root=0)
        # 初始化每个进程接收的数据大小
        recvbuf2 = np.zeros(count2[rank])
        comm.Scatterv([sendbuf2, count2, displ2, MPI.DOUBLE], recvbuf2, root=0)

        # print('After Scatterv, process {} has data:'.format(rank), recvbuf1, recvbuf2)
        recvbuf1 = recvbuf1.reshape(-1, self._c1)
        recvbuf2 = recvbuf2.reshape(self._c1, -1)
        result = np.zeros((recvbuf1.shape[0], recvbuf2.shape[1]))
        temp = 0
        for i in range(recvbuf1.shape[0]):
            for k in range(recvbuf2.shape[1]):
                for j in range(recvbuf1.shape[1]):
                    temp = self._m1[i,j] * self._m2[j,k]
                result[i,k] = temp
        end = time.time()
        print(nprocs, ' process: ', end-since)


if __name__ == "__main__":

    # 超参数 定义矩阵的维度
    # 第一个矩阵的行
    ROW1 = 256
    # 第一个矩0阵的列
    COL1 = 248
    # 第二个矩阵的列
    COL2 = 235

    # 先生成文件
    data = DATA(ROW1, COL1, COL2)

    # 获取两个随机矩阵
    m1, m2 = data.gene_data()

    # 创建矩阵乘法的实例
    op = MatrixMultiply(m1, m2)

    # 串行乘法
    # op.single_multiply()

    # MPI 并行乘法 
    op.multiprocesses_multi()
